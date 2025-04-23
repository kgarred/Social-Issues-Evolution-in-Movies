import middleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random
import time

# customized class to handle retries for default error codes with exponential backoff timer
class CustomRetryMiddleware(RetryMiddleware):
    # override
    def __init__(self, settings):
        self.download_delay = settings.getfloat('DOWNLOAD_DELAY')
        super().__init__(settings)
        
    # override
    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            
            # Exponential Backoff (with Jitter)
            retry_times = request.meta.get('retry_times', 0)
            sec = (2 ** retry_times) + round(random.random(), 4)
            spider.logger.info(' Retrying: {} ({} times, wait +{} sec)'.format(spider.name, retry_times + 1, sec))
            time.sleep(sec + self.download_delay)
            
            return self._retry(request, reason, spider) or response
        return response
        