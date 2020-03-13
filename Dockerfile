FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
RUN pip install gunicorn
WORKDIR /app/urlshortener

EXPOSE 8080
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-p", "8080"]
