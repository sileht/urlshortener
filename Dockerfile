FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
WORKDIR /app/urlshortener

EXPOSE 8080
CMD [ "uvicorn", "--port", "8080", "main:app"]
