import scrapy
import sys
import os
import logging
sys.path.append(os.environ['PYTHONPATH'])
from util_time import TimeUtil

class HgSpider(scrapy.Spider):
    name = 'hg3'
    allowed_domains = ['csdn.net']
    start_urls = ['https://hellogithub.blog.csdn.net/article/list/1']
    page_url = 'https://hellogithub.blog.csdn.net/article/list/{}'
    num_in_page = 40

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    custom_settings = {
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy_common.middlewares.ChromeDownloaderMiddleware': 543,
        # },
        'ITEM_PIPELINES': {
            # 'csdn.pipelines.CsdnWriteTextPipeline': 100,
            'csdn.pipelines.CsdnWriteJsonPipeline': 200,
        },
        'DOWNLOAD_DELAY': 0.5,
        'LOG_ENABLED': True,
        # 'LOG_LEVEL': logging.
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_save_dir = '/Users/zxzx/Documents/csdn_blogs/{}-{}'.format(TimeUtil.get_date_stamp(),'hello_github')
        self.json_save_file = '/Users/zxzx/Documents/csdn_blogs/{}-{}.jl'.format(TimeUtil.get_date_stamp(),'hello_github')

    def parse(self, response):
        r = response
        author = r.xpath('//div[@class="profile-intro-name-boxTop"]/a[1]/@title').extract_first()
        posts = r.xpath('//div[@class="article-list"]/div')
        for post in posts:
            url = post.xpath('./h4/a/@href').extract_first()
            type = post.xpath('./h4/a/span[contains(@class, "article-type")]/text()').extract_first()
            try:
                title = post.xpath('./h4/a/text()').re('^\s*(.+)\s*$')[1]
            except:
                title = '标题解析失败'
            date_ = post.xpath('.//span[@class="date"]/text()').extract_first()
            read_num = post.xpath('.//span[@class="read-num"][1]/text()').extract_first()
            comment_num = post.xpath('.//span[@class="read-num"][2]/text()').extract_first()
            item = {
                'url': url,
                'type': type,
                'title': title,
                'date': date_,
                'read_num': read_num,
                'comment_num': comment_num,
                'crawl_date': TimeUtil.get_time_stamp(),
                'author': author
            }
            yield scrapy.Request(url=url, meta={'item':item}, callback=self.parse_detail)
        # 多页爬取
        cnt = r.xpath('//ul[@class="container-header-ul"]/li[1]/span/text()').re_first('\d+')
        cnt = int(cnt)
        page = cnt // self.num_in_page + 1
        for i in range(2, page+1):
            yield scrapy.Request(url=self.page_url.format(i))

    def parse_detail(self, response):
        r = response
        html1 = r.xpath('//div[@id="article_content"]').extract_first()
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        source_md = h.handle(html1)
        item = response.meta['item']
        item['source_md'] = source_md
        yield item

