import scrapy
import sys
import os
import logging
from util_time import TimeUtil

class HgSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/xueweihan/default.html?page=1']
    page_url = 'https://www.cnblogs.com/xueweihan/default.html?page={}'
    num_in_page = 14

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    custom_settings = {
        'ITEM_PIPELINES': {
            'csdn.pipelines.CsdnWriteJson2Pipeline': 200,
        },
        'DOWNLOAD_DELAY': 0.5
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_save_dir = '/Users/zxzx/Documents/cnblogs/{}-{}'.format(TimeUtil.get_time_stamp(),'hello_github')
        self.json_save_file = '/Users/zxzx/Documents/cnblogs/{}-{}.jl'.format(TimeUtil.get_time_stamp(),'hello_github')


    def parse(self, response):
        r = response
        author = '削微寒'
        posts = r.xpath('//*[@id="mainContent"]/div/div[@class="day"]')
        for post in posts:
            url = post.xpath('.//a[contains(@class, "postTitle2")]/@href').extract_first()
            type = ''
            try:
                title = post.xpath('.//a[contains(@class,"postTitle2")]/span/text()').extract()
                title = ''.join(title)
                title = title.strip()
            except:
                title = 'title解析失败'
            date_ = post.xpath('.//div[contains(@class, "postDesc")]/text()').re_first('(20\d+\-\d+\-\d+ \d+:\d+)')
            read_num = post.xpath('.//div[contains(@class, "postDesc")]/span[@class="post-view-count"]').re_first('阅读\(((\d+))\)')
            comment_num = post.xpath('.//div[contains(@class, "postDesc")]/span[@class="post-comment-count"]').re_first('评论\(((\d+))\)')
            recommend_num = post.xpath('.//div[contains(@class, "postDesc")]/span[@class="post-digg-count"]').re_first('推荐\(((\d+))\)')
            item = {
                'url': url,
                'type': type,
                'title': title,
                'date': date_,
                'read_num': read_num,
                'comment_num': comment_num,
                'recommend_num': recommend_num,
                'crawl_date': TimeUtil.get_time_stamp(),
                'author': author
            }
            yield item
            # yield scrapy.Request(url=url, meta={'data':item}, callback=self.parse_detail)

        # 多页爬取
        has_nxt = r.xpath('//div[@id="nav_next_page"]/a')
        if has_nxt:
            nxt_page = r.xpath('//div[@id="nav_next_page"]/a/@href').extract_first()
            yield scrapy.Request(url=nxt_page)
        else:
            str1 = r.xpath('//div[@id="homepage_bottom_pager"]/div[@class="pager"]/a[last()]/text()').extract_first()
            if str1 == '下一页':
                nxt_page = r.xpath('//div[@id="homepage_bottom_pager"]/div[@class="pager"]/a[last()]/@href').extract_first()
                yield scrapy.Request(url=nxt_page)

    def parse_detail(self, response):
        r = response
        item = response.meta['data']
        yield item