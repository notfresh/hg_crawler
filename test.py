from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    execute([
        "scrapy", "crawl", "cnblogs"
    ])