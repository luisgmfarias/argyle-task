FROM python:3.9

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
WORKDIR /usr/local/

COPY requirements.txt ./
RUN mkdir output
COPY models ./
COPY scraper ./
COPY tests ./
COPY app.py ./
COPY wsgi.py ./
COPY README.md ./
COPY .login.json ./

RUN pip install -r ./requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]



