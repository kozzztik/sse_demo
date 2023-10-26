FROM python:3.11
EXPOSE 7000
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/sse_demo
WORKDIR /opt/sse_demo

RUN pip install --upgrade pip
ADD requirements.txt /opt/sse_demo/requirements.txt

# update requirements
RUN pip install -r requirements.txt

ADD sse_demo /opt/sse_demo/sse_demo
ADD server_key.crt /opt/sse_demo/server_key.crt
ADD server_key.key /opt/sse_demo/server_key.key
ADD asgi.py /opt/sse_demo/asgi.py

ADD manage.py /opt/sse_demo/manage.py
ADD worker.py /opt/sse_demo/worker.py

ADD gunicorn.conf.py /opt/sse_demo/gunicorn.conf.py
CMD [ "gunicorn" ]
