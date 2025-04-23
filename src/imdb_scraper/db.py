# -*- coding: utf-8 -*-

"""
DB management
"""
import sqlite3
import pandas as pd
import zlib

def open_sqlite(db_fn):
    """ Open connection to sqlite local DB """
    conn = sqlite3.connect(db_fn)
    return conn

def compress_string(a):
    return zlib.compress(a.encode())

def decompress_string(z):
    return zlib.decompress(z).decode()

def create_page_dump(db_conn):
    """ create table for Google page dump """
    c = db_conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS pages_dump 
            (url text PRIMARY KEY, 
            film_id text,
            page_content_zip blob NOT NULL,
            page_nchar int NOT NULL,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP)
            ;
            ''')
    db_conn.commit()
    print('create_page_dump')


def insert_page(db_conn, url, film_id, page_content, nchar):
    c = db_conn.cursor()
    sql = '''INSERT INTO pages_dump(url, film_id, page_content_zip, page_nchar)
              VALUES(?,?,?,?) '''
    cur = db_conn.cursor()
    cur.execute(sql, [url, film_id, compress_string(page_content), nchar])
    db_conn.commit()
    return db_conn


def run_select_sql(sql, db_conn):
    """ Run SQL select on db and return data frame. """
    assert sql
    assert db_conn
    df = pd.read_sql(sql, db_conn)
    return df


def check_dbconnection_status(db_conn):
    assert db_conn
    if not db_conn.closed == 0:
        raise RuntimeError('Connection to DB is closed, it should be open!')
    return True


def does_dump_table_exist(db_conn):
    assert db_conn
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='pages_dump';"
    df = run_select_sql(sql, db_conn)
    return not df.empty


def url_exists(con, targeturl):
    df = pd.read_sql("SELECT * from pages_dump WHERE url==\""+targeturl+"\"", con)

    if(df.empty):
        return False
    return True

def make_string_sql_safe(s):
    """ Escape quotes """
    s = s.replace("'","''")
    return s


def scan_table_limit_offset(db_conn, select_sql, block_sz, funct):
    print('scan_table_limit_offset')
    offset = 0
    keep_scanning = True
    while keep_scanning:
        print('  offset =',offset)
        sql = "{} limit {} offset {};".format(select_sql, block_sz, offset)
        results_df = pd.read_sql(sql, db_conn)
        funct(results_df)
        # scanning logic
        offset += block_sz
        if len(results_df) < block_sz:
            keep_scanning = False
    