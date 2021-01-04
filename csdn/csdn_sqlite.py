from common.connection_manager import ConnectionManager
from img_url_crawler.util.util_logging import logger


class CSDN:
    table_name = 'csdn'

    @classmethod
    def create_table(cls):
        connections = ConnectionManager.get_all_connections()
        for conn in connections:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    ("create table {}(" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "url text, " +
                    "type text, " +
                    "title text, " +
                    "date text " +
                    "read_num INTEGER, " +
                    "crawl_date text, " +
                    "author text, " +
                    ")").format(cls.table_name)
                )
                logger.info("{} 表创建成功".format(cls.table_name))
            except Exception as e:
                logger.error(e)
        # 创建重复数据表


    @classmethod
    def insert(cls, desc, page_url, img_url):
        conn = ConnectionManager.get_connection()
        cursor = conn.cursor()
        try:
            logger.info("插入 {} 表".format(cls.table_name))
            cursor.execute(("insert into {}("
                            "type, img_url, "
                            "img_url, img_url, img_url, img_url,"
                            ") " +
                           "values (?,?,?)").format(cls.table_name),
                           (desc, page_url, img_url))
            conn.commit()  # - -插入完之后提交
        except Exception as e:
            logger.error(e)

    # @classmethod
    # def select_by_id(cls, id):
    #     connections = ConnectionManager.get_all_connections()
    #     res = []
    #     for conn in connections:
    #         cursor = conn.cursor()
    #         try:
    #             cursor.execute("select desc, page_url, img_url from {} where id={} limit 1".format(cls.table_name, id))
    #             res1 = cursor.fetchall()
    #             res1 = [ \
    #                 {'desc': item[0], 'page_url':item[1], 'img_url': item[2]} \
    #                 for item in res1 \
    #             ]
    #             res.extend(res1)
    #         except Exception as e:
    #             logger.error(e)
    #             return res
    #     return (res[0] if res != [] else None)
