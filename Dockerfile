FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
WORKDIR /app/urlshortener

EXPOSE 8000
CMD [ "uvicorn", "main:app"]
