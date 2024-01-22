FROM python:3.9.1

RUN pip install pyarrow pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]

# docker build -t test:python .
# docker run -it test:python 2024-01-23
