FROM python:3.9
COPY requrements.txt .
RUN pip install -r requrements.txt
COPY .env .
COPY ./scr/nyc-taxi/* ./
COPY ./data/. ./
EXPOSE 80
ENTRYPOINT ["python", "./main.py"]
