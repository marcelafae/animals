FROM python:3.10.6-buster

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# Install Animal_adoption!
COPY Animal_Adoption Animal_Adoption
COPY setup.py setup.py
RUN pip install .


CMD uvicorn Animal_Adoption.api.fast:app --host 0.0.0.0
