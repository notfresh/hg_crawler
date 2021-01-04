

class ESTool:

    from elasticsearch import Elasticsearch
    from datetime import datetime
    es = Elasticsearch()
    iname = "csdn2"

    @classmethod
    def create_index_and_mapping(cls):
        iname = cls.iname
        mapping = {
            'properties': {
                'title': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_max_word'
                }
            }
        }
        cls.es.indices.create(index=iname, ignore=400)
        result = cls.es.indices.put_mapping(index=iname, body=mapping)
        # print(result)

    @classmethod
    def write(cls, dict_):
        result = cls.es.index(index=cls.iname, body=dict_)
        # print(result)


if __name__ == '__main__':
    ESTool.create_index_and_mapping()

