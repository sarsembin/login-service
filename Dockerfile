FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /login-app
COPY requirements.txt /login-app/requirements.txt
RUN pip install -r requirements.txt
COPY . /login-app/

CMD python3.8 manage.py runserver 0.0.0.0:8000