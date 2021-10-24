FROM python:3.10-slim-bullseye
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt .
RUN \
	apt-get update && \
	apt-get install -y libpq-dev && \
	pip install -r requirements.txt
COPY src .
CMD [ "python", "/app/simple_small_api.py" ]
EXPOSE 80
