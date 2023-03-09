FROM tensorflow/tensorflow:2.10.0

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# Install Animal_adoption!
COPY Animal_Adoption Animal_Adoption
COPY setup.py setup.py
RUN pip install .

# We already have a make command for that!
#COPY Makefile Makefile
RUN make reset_local_files

CMD uvicorn Animal_Adoption.api.fast:app --host 0.0.0.0
