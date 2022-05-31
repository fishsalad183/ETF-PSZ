# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from logging.handlers import RotatingFileHandler
from scrapy.utils.log import configure_logging

csv_file_path = 'db/scrapy_vozila.csv'

LOG_ENABLED = False
# Disable default Scrapy log settings
configure_logging(install_root_handler=False)
# Define own logging settings
log_file = 'scraper/tmp/log.txt'    # NOTE: The first directory is 'scraper' to enable starting scrapy from the directory above, i.e. the root directory
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_file_log = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=1, encoding='utf-8')
rotating_file_log.setFormatter(formatter)
root_logger.addHandler(rotating_file_log)

# LOG_ENABLED = True
# LOG_FILE = 'scraper/tmp/log.txt'  # NOTE: The first directory is 'scraper' to enable starting scrapy from the directory above, i.e. the root directory!
# LOG_LEVEL = 'DEBUG'
FEED_EXPORT_ENCODING = 'utf-8'


BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.scraper.spiders']    # NOTE: Changed from scraper.spiders to scraper.scraper.spiders to enable starting scrapy from the directory above, i.e. the root directory!
NEWSPIDER_MODULE = 'scraper.scraper.spiders'    # NOTE: Changed from scraper.spiders to scraper.scraper.spiders to enable starting scrapy from the directory above, i.e. the root directory!


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scraper.middlewares.ScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'scraper.middlewares.ScraperDownloaderMiddleware': 543,
}


# For the scrapy-rotating-proxies package
DOWNLOADER_MIDDLEWARES.update({
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
})
ROTATING_PROXY_LIST_PATH = 'proxies/proxies.txt'


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'scraper.scraper.pipelines.MySQLStorePipeline': 300, # NOTE: Changed from scraper.pipelines.MySQLStorePipeline to scraper.scraper.pipelines.MySQLStorePipeline to enable starting scrapy from the directory above, i.e. the root directory!
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
# For rotating user agents (requires pip install scrapy-useragents)
# See https://python.plainenglish.io/rotating-user-agent-with-scrapy-78ca141969fe
DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
})
USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0')  # firefox
]