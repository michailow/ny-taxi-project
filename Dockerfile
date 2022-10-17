FROM python:3.9
COPY requrements.txt .
RUN pip install -r requrements.txt
COPY .env .
COPY ./scr/nyc-taxi/* ./
COPY ./data/yellow_tripdata_2022-05.parquet ./
EXPOSE 80
ENTRYPOINT ["python", "./main.py"]
