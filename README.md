# Social Issues Evolution in Movies

This project explores the evolution of social issues in movies over time, using data from IMDb. It involves data collection, preprocessing, feature extraction, supervised machine learning, and geo-spatial/temporal analysis to classify movies into predefined social issue categories.

---

### Directory Structure

```
e:\Dissertation\Social-Issues-Evolution-in-Movies
│
├── data/                     # Contains datasets, raw and processed data
├── notebooks/                # Jupyter notebooks for exploration and modeling
├── src/                      # Source code for data collection, preprocessing, and analysis
├── reports/                  # Reports and documentation
├── tests/                    # Unit tests for the source code
├── references/               # Research papers and related references
├── README.md                 # Project overview and instructions
├── requirements.txt          # Python dependencies
└── .gitignore                # Git ignore file
```

---

### Methodology

The workflow process consists of the following steps:

#### Step 1: Data Collection
- **Description**: Data was scraped and stored from IMDb webpages.
- **Data Size**: 100,000 movies.
- **Code Location**: `src/imdb_scraper/`

#### Step 2: Data Preprocessing
- **Description**: Data cleaning, defining social issue labels, and manual labeling using the RAG system with Llama3 and LangChain.
- **Code Location**: `src/preprocessing/`

#### Step 3: Feature Creation
- **Description**: Extracted features using sentence transformer embeddings and sentiment scores from movie summaries.
- **Code Location**: `src/analysis/`

#### Step 4: Model Development
- **Description**: Developed a supervised machine learning model (SVM) to classify movies into 13 categories using summary embeddings and sentiment scores as input features.
- **Code Location**: `notebooks/modeling/`

#### Step 5: Classification
- **Description**: Classified unlabelled movies with predefined social issue labels using the trained SVM model.
- **Code Location**: `src/analysis/`

#### Step 6: Model Evaluation
- **Description**: Evaluated the model's performance on the testing set using metrics like balanced accuracy, macro precision, recall, F1-score, and ROC-AUC curve.
- **Results**: Achieved a mean accuracy of **72% ± 0.02**.
- **Code Location**: `notebooks/modeling/`

#### Step 7: Geo-Spatial and Temporal Analysis
- **Description**: Analyzed time and space-related patterns across movies.
- **Code Location**: `src/visualization/`

---

### Visualizations

The project includes various visualizations to:
- Highlight how certain social issues gained focus over time.
- Reveal opportunities in genres where social issues could be more diversified.

**Code Location**: `src/visualization/`

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Social-Issues-Evolution-in-Movies.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Social-Issues-Evolution-in-Movies
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Usage

1. **Data Collection**: Run the IMDb scraper to collect data:
   ```bash
   python src/imdb_scraper/
   ```
2. **Preprocessing**: Clean and preprocess the data:
   ```bash
   python src/data_preprocessing.ipynb
   ```
3. **Feature Extraction**: Generate embeddings and sentiment scores:
   ```bash
   python src/Create_Features.ipynb
   ```
4. **Model Training**: Train the SVM model:
   ```bash
   jupyter src/SVM_classification.ipynb
   ```
5. **Visualization**: Generate visualizations:
   ```bash
   python reports/
   ```

---

### References

- IMDb Dataset
- Research papers and articles on social issues in movies.

---

### Contributions

Feel free to contribute by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

### License

This project is licensed under the MIT License. See `LICENSE` for details.
