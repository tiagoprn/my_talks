"""
Given a csv file, generates a json file and then iterates through each one of
its' lines. Uses pandas to help with reading the CSV and converting it into a
json file.

Then, we use a python iterator to read the lines from the file and feed them to
the elasticsearch bulk insert API.


If you are running with the Makefile, you must download the kaggle videogame
sales dataset csv file at https://www.kaggle.com/gregorut/videogamesales/download
and change CSV_PATH on the Makefile to the full path where you have downloaded it.
"""

import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import requests

import pandas as pd
import typer
from elasticsearch import Elasticsearch, helpers

LOG_FORMAT = (
    '[%(asctime)s PID %(process)s '
    '%(filename)s:%(lineno)s - %(funcName)s()] '
    '%(levelname)s -> \n'
    '%(message)s\n'
)
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout),],
)
logger = logging.getLogger(__name__)


def open_input_json_file(json_file: str):
    with open(json_file, 'r') as input_file:
        for record in input_file:
            yield record.replace('\n', '')


def populate(csv_file: Path):
    logger.info(f'Running for file={csv_file}...')

    if not csv_file.is_file() or (not csv_file.exists()):
        logger.info('This is not a valid file or it does not exist.')
        sys.exit(1)

    dataset_name = csv_file.name.split('.')[0]

    json_file = f"{str(Path.home())}/tmp/{dataset_name}.json"

    json_file_exists = Path(json_file).exists()

    if not json_file_exists:
        dataframe = pd.DataFrame()

        CHUNKSIZE = 10000

        chunk_number = 0

        logger.info('Computing CSV file number of lines...')
        try:
            num_lines = sum(1 for line in open(csv_file.as_posix()))
            encoding = 'utf-8'
        except UnicodeDecodeError:
            num_lines = sum(
                1 for line in open(csv_file.as_posix(), encoding='latin-1')
            )
            encoding = 'latin-1'

        csv_size = csv_file.stat().st_size

        chunks = math.ceil((num_lines - 1) / CHUNKSIZE)

        with open(json_file, 'w') as file:
            logger.info(
                f'Reading CSV into a pandas dataframe '
                f'(lines={num_lines}, file_size={csv_size})...'
            )
            dfs = pd.read_csv(
                csv_file,
                encoding=encoding,
                error_bad_lines=False,
                chunksize=CHUNKSIZE,
            )
            for chunk_number, df in enumerate(dfs):
                chunk_number += 1
                logger.info(f'Processing chunk {chunk_number}/{chunks}...')
                df.to_json(file, orient='records', lines=True)
                file.write('\n')

    logger.info('Initializing Elasticsearch...')

    es = Elasticsearch()

    key = (
        {
            "_index": f'{dataset_name}_index',
            "_type": f'{dataset_name}_index_doctype',
            "_source": record,
        }
        for record in open_input_json_file(json_file)
    )
    helpers.bulk(es, key)

    logger.info('Finished.')


if __name__ == '__main__':
    typer.run(populate)
