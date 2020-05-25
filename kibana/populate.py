import json
import logging

from uuid import uuid4

from datetime import datetime

from elasticsearch import Elasticsearch
import requests


logger = logging.getLogger(__name__)


def main():
    logger.info('Initializing Elasticsearch...')

    es = Elasticsearch()

    records = []

    for dict_data in records:
        res = es.index(index='pokemon_index',
                    doc_type='pokemon_index_doctype',
                    id=uuid4(),
                    body=dict_data)
        logger.info(res['result'])

if __name__ == '__main__':
    main()
