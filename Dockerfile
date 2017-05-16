FROM django
ADD . /v-crew

WORKDIR /v-crew

#RUN apt-get update && apt-get install -y git
RUN pip install -r ./requirements/base.txt
