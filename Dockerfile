FROM python:3.8.2

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-dev \
    python3-pip\
    python-psycopg2 \
    git \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install crf++
RUN git clone https://github.com/mtlynch/crfpp.git
RUN cd crfpp && \
    ./configure && \
    make && \
    make install && \
    ldconfig

ADD . /code
WORKDIR /code

# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

EXPOSE 8000
