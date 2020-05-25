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

    dataframe= pd.DataFrame()

    CHUNKSIZE = 100000

    chunk_number = 0
    try:
        for chunk in pd.read_csv(csv_file, error_bad_lines=False, chunksize=CHUNKSIZE):
            dataframe = pd.concat([dataframe, chunk], ignore_index=True)
            chunk_number += 1
            logger.info(f'Finished processing chunk {chunk_number}')
            if chunk_number == 1:
                break  # TODO: remove, just testing here....
    except UnicodeDecodeError:
        for chunk in pd.read_csv(
            csv_file, encoding='latin-1', error_bad_lines=False, chunksize=CHUNKSIZE
        ):
            dataframe = pd.concat([dataframe, chunk], ignore_index=True)
            chunk_number += 1
            logger.info(f'Finished processing chunk {chunk_number}')
            if chunk_number == 1:
                break  # TODO: remove, just testing here....

    logger.info('Converting dataframe to json file...')

    dataframe.to_json(json_file, orient='records', lines=True)

    logger.info('Initializing Elasticsearch...')

    es = Elasticsearch()

    with open(json_file, 'r') as input_file:
        records = input_file.readlines()

    for data in records:
        dict_data = json.loads(data.replace('\n', ''))
        res = es.index(index=f'{dataset_name}_index',
                    doc_type=f'{dataset_name}_index_doctype',
                    body=dict_data)
        logger.info(res['result'])

if __name__ == '__main__':
    typer.run(populate)

