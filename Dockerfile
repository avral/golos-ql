FROM python:3.6.4

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD . /app

# Development
# CMD flask run --host=0.0.0.0

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
