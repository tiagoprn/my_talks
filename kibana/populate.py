import json
import logging
import sys

from pathlib import Path
from uuid import uuid4

from datetime import datetime

from elasticsearch import Elasticsearch
import pandas as pd
import requests
import typer

LOG_FORMAT = ('[%(asctime)s PID %(process)s '
              '%(filename)s:%(lineno)s - %(funcName)s()] '
              '%(levelname)s -> \n'
              '%(message)s\n')
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ])
logger = logging.getLogger(__name__)


def populate(csv_file: Path):
    logger.info(f'Running for file={csv_file}...')

    if not csv_file.is_file() or (not csv_file.exists()):
        logger.info('This is not a valid file or it does not exist.')
        sys.exit(1)

    dataset_name = csv_file.name.split('.')[0]

    json_file = csv_file.as_posix().replace('.csv', '.json')

    dataframe = pd.read_csv(csv_file)
    dataframe.to_json(json_file, orient='records')

    logger.info('Initializing Elasticsearch...')

    es = Elasticsearch()

    records = []

    for dict_data in records:
        res = es.index(index=f'{dataset_name}_index',
                    doc_type=f'{dataset_name}_index_doctype',
                    body=dict_data)
        logger.info(res['result'])

if __name__ == '__main__':
    typer.run(populate)

