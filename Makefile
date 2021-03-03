# Variables
LOCAL_DATA_PATH='raw_data/ocr_labeled_spellcheck.csv'
PROJECT_ID='wagon-bootcamp-305111'
BUCKET_NAME='wagon-ml-ramsyy-00'
BUCKET_DATA_FILE='data/ocr_labeled_spellcheck.csv'
BUCKET_MODEL_FILE='model/v1/ridge'

JOB_NAME=full_training_$(shell date +'%Y%m%d_%H%M%S')
BUCKET_TRAINING_FOLDER='trainings'
PACKAGE_NAME='OpenFoodFacts'
PYTHON_VERSION='3.7'
RUNTIME_VERSION='2.4'

REGION='europe-west1'

# GCP methods#

set_project:
	-@gcloud config set project ${PROJECT_ID}

create_bucket:
	-@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	-@gsutil cp ${LOCAL_DATA_PATH} gs://${BUCKET_NAME}/${BUCKET_DATA_FILE}

download_data:
	-@python OpenFoodFacts/data.py

train_local:
	-@python OpenFoodFacts/trainer.py

train_gcp:
	-@gcloud ai-platform jobs submit training ${JOB_NAME} \
	  --job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER}  \
	  --package-path ${PACKAGE_NAME} \
	  --module-name ${PACKAGE_NAME}.trainer \
	  --python-version=${PYTHON_VERSION} \
	  --runtime-version=${RUNTIME_VERSION} \
	  --region ${REGION} \
	  --stream-logs


# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* OpenFoodFacts/*.py

black:
	@black scripts/* OpenFoodFacts/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr OpenFoodFacts-*.dist-info
	@rm -fr OpenFoodFacts.egg-info

install:
	@pip install . -U

all: clean install test black check_code


uninstal:
	@python setup.py install --record files.txt
	@cat files.txt | xargs rm -rf
	@rm -f files.txt

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)
