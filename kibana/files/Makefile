.PHONY: help
SHELL:=/bin/bash
SHARED_FOLDER=/tmp/shared-docker-$(shell date +%Y%m%d_%H%M%S)
ROOT_FOLDER=$(shell pwd)
CURRENT_FOLDER=current
DFT_FOLDER=dft

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


raise:  ## temporary configuration to allow running the elasticsearch containers
	@sudo sysctl -w vm.max_map_count=262144

docker-compose-dft-up: clean raise  ## Up docker-compose for development
	@cd $(ROOT_FOLDER)/$(DFT_FOLDER) && docker-compose up -d

docker-compose-dft-stop: clean  ## Stop docker-compose for development
	@cd $(ROOT_FOLDER)/$(DFT_FOLDER) && docker-compose stop

docker-compose-dft-rm: docker-compose-dft-stop  ## Delete the development environment containers
	@cd $(ROOT_FOLDER)/$(DFT_FOLDER) && docker-compose rm -f

docker-compose-current-up: clean raise  ## Up docker-compose for development
	@cd $(ROOT_FOLDER)/$(CURRENT_FOLDER) && docker-compose up -d

docker-compose-current-stop: clean  ## Stop docker-compose for development
	@cd $(ROOT_FOLDER)/$(CURRENT_FOLDER) && docker-compose stop

docker-compose-current-rm: docker-compose-current-stop  ## Delete the development environment containers
	@cd $(ROOT_FOLDER)/$(CURRENT_FOLDER) && docker-compose rm -f

nodes-info:  ## Get if the cluster is running successfully
	@curl -X GET "localhost:9200/_cat/nodes?v&pretty"

healthcheck:  ## Get if the cluster is running successfully
	@curl -X GET "localhost:9200/_cat/health?v&pretty"

kibana:  ## Opens kibana dashboard
	@xdg-open http://localhost:5601/

