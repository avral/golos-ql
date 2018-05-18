FROM python:3.6.4

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app


#COPY . /app
#WORKDIR /app
#
#RUN pip install -r requirements.txt
#
#WORKDIR /app
