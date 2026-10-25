#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = ccds-dsip-exercise-repo
PYTHON_VERSION = 3.14
PYTHON_INTERPRETER = uv run python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	uv sync
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint
lint:
	$(PYTHON_INTERPRETER) -m flake8 src
	$(PYTHON_INTERPRETER) -m isort --check --diff src
	$(PYTHON_INTERPRETER) -m black --check src

## Format source code with black
.PHONY: format
format:
	$(PYTHON_INTERPRETER) -m isort src
	$(PYTHON_INTERPRETER) -m black src



## Run tests
.PHONY: test
test:
	$(PYTHON_INTERPRETER) -m pytest tests
## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	aws s3 sync s3://itudsip/data/ \
		data/ 
	

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	aws s3 sync data/ \
		s3://itudsip/data 
	



## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Run the full pipeline: data -> features -> train -> predict
.PHONY: pipeline
pipeline:
	$(MAKE) requirements
	$(MAKE) data
	$(MAKE) features
	$(MAKE) train
	$(MAKE) predict

## Make dataset
.PHONY: data
data: dataset

.PHONY: dataset
dataset:
	$(PYTHON_INTERPRETER) src/dataset.py

## Make features
.PHONY: features
features:
	$(PYTHON_INTERPRETER) src/features.py

## Train a model
.PHONY: train
train:
	$(PYTHON_INTERPRETER) src/modeling/train.py

## Run inference with the trained model
.PHONY: predict
predict:
	$(PYTHON_INTERPRETER) src/modeling/predict.py

## Generate plots
.PHONY: plots
plots:
	$(PYTHON_INTERPRETER) src/plots.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
