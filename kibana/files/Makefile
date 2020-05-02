.PHONY: help
SHELL:=/bin/bash
SHARED_FOLDER=/tmp/shared-docker-$(shell date +%Y%m%d_%H%M%S)


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

docker-compose-up: clean raise  ## Up docker-compose for development
	@docker-compose up -d

docker-compose-stop: clean  ## Stop docker-compose for development
	@docker-compose stop

docker-compose-rm: docker-compose-stop  ## Delete the development environment containers
	@docker-compose rm -f

docker-compose-logs: clean  ## See all containers logs in real-time
	@docker-compose logs

check:  ## Get if the cluster is running successfully
	@curl -X GET "localhost:9200/_cat/nodes?v&pretty"

kibana:  ## Opens kibana dashboard
	@xdg-open http://localhost:5601/

