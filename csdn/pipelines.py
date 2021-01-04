# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import json
import os

class CsdnWriteJsonPipeline:
    def open_spider(self, spider):
        self.writer = open(spider.json_save_file, mode='w+', encoding='utf-8')

    def process_item(self, item, spider):
        item_part = {
            'title': item['title'],
            'url': item['url'],
            'read_num': item['read_num']
        }
        self.writer.write('{}\n'.format(json.dumps(item_part, ensure_ascii=False)))
        return item

    def close_spider(self, spider):
        self.writer.close()


class CsdnWriteTextPipeline:

    def process_item(self, item, spider):
        save_path = spider.text_save_dir
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        with open(os.path.join(save_path, '{}.md'.format(item['title'])), 'w+', encoding='utf-8') as file:
            file.write(
                '标题: {}\n'.format(
                    item.get('title', '无标题'),
                )
            )
            file.write(
                '作者: {}\n'.format(
                    item.get('author', '无'),
                )
            )
            file.write(
                '{}\n'.format(
                    item.get('source_md', '无'),
                )
            )

        return item


class Csdn_ES_Pipeline:

    def open_spider(self, spider):
        from csdn.es_tool import ESTool
        self.writer = ESTool()

    def process_item(self, item, spider):
        import json
        self.writer.write(item)
        return item



