"""
Uses the Pokemon API to get information on the pokemons on each generation.

Build a list of dicts with one record per generation, with information of which pokemon are on each
generation. Then, each dict is feed sequentially to the elasticsearch API index method, that
persists each record one by one.
"""


import json
import logging
from datetime import datetime
from uuid import uuid4

import requests

from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

ROOT_URL = 'https://pokeapi.co/api/v2'
GENERATIONS_URL_TEMPLATE = '{url}/generation/{generation_id}'
TEMP_FILE = '/tmp/pokemons.json'


def get_generations_data():
    logger.info('Getting generation data...')

    generations = []

    for index in range(9):
        generation_number = index + 1
        logger.info(f'Processing generation {generation_number}...')

        generation_url = GENERATIONS_URL_TEMPLATE.format(
            url=ROOT_URL, generation_id=generation_number
        )
        response = requests.get(generation_url)
        if response.status_code == 404:
            logger.info(
                f'Stopping iteration, there is '
                f'no generation {generation_number} yet.'
            )
            break

        response_data = response.json()

        generation = {
            'number': generation_number,
            'name': response_data['main_region']['name'],
        }
        pokemons = []

        for pokemon in response_data['pokemon_species']:
            pokemons.append(pokemon['name'])

        generation.update({'pokemons': pokemons})

        generations.append(generation)

    with open(TEMP_FILE, 'w') as output_file:
        output_file.write(json.dumps(generations))

    logger.info('Finished.')

    return generations


def main():
    logger.info('Initializing Elasticsearch...')

    es = Elasticsearch()

    records = get_generations_data()

    for dict_data in records:
        res = es.index(
            index='pokemon_index',
            doc_type='pokemon_index_doctype',
            id=uuid4(),
            body=dict_data,
        )
        logger.info(res['result'])


if __name__ == '__main__':
    main()
