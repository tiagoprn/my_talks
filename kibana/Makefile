.PHONY: help
SHELL:=/bin/bash
ROOT_FOLDER=$(shell pwd)

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, optimized files, logs, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -fr .pytest_cache/
	@rm -f coverage.xml
	@rm -f *.log
	@find . -name "celerybeat-schedule*" | xargs rm -rf


populate-simple:  ## populate kibana from the pokemon API
	@python simple.py

populate-bulk: ## populate kibana from the videogame sales csv
	@python bulk.py /storage/datasets/kibana-presentation/videogame-sales.csv

present:  ## display the presentation
	@mdp presentation.md

kibana-nodes-info:  ## Get the kibana cluster nodes info
	@curl -X GET "localhost:9200/_cat/nodes?v&pretty"

kibana-healthcheck:  ## Get the kibana cluster health
	@curl -X GET "localhost:9200/_cat/health?v&pretty"

kibana-dashboard:  ## Opens kibana dashboard
	@xdg-open http://localhost:5601/

