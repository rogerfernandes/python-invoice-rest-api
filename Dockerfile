FROM python:3.7-slim

RUN python -m pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app
COPY . /app

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 80
CMD /wait && command python app.py
