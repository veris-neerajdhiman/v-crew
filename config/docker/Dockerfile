FROM django

WORKDIR /v-crew

ADD ./requirements/base.txt /v-crew/requirements/base.txt

RUN apt-get update && apt-get install -y git
RUN pip install -r ./requirements/base.txt

ADD . /v-crew

EXPOSE 80

COPY ./config/docker/docker-entrypoint.sh /
ENTRYPOINT ["./config/docker/docker-entrypoint.sh"]