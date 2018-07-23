FROM python:3.6-slim-stretch

COPY . /app_manager/

RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list  && \
#RUN apt update && \
    echo `ls /app_manager/` && \
    apt update && \
    apt install -y netcat gcc && \
#    pip install --no-cache-dir -r /app_manager/sanic_manager/requirements
    pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r /app_manager/sanic_manager/requirements && \
    apt autoremove -y


WORKDIR /app_manager/sanic_manager

VOLUME /app_manager/sanic_manager/uploads

CMD ["./start.sh"]