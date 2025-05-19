FROM erlang:26-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    autoconf \
    automake \
    libexpat1-dev \
    libxml2-dev \
    libncurses5-dev \
    perl \
    wget \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

ENV TSUNG_VERSION=v1.7.0

RUN git clone https://github.com/processone/tsung.git /opt/tsung && \
    cd /opt/tsung && \
    git checkout $TSUNG_VERSION && \
    ./configure && \
    make && \
    make install

WORKDIR /tsung

COPY ./*.xml ./scenarios/

CMD ["tail", "-f", "/dev/null"]
