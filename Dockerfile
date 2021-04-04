FROM python:3.7

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install requests
RUN pip install -r requirements.txt

COPY ./server /app

WORKDIR /app
CMD ["python","app.py"]