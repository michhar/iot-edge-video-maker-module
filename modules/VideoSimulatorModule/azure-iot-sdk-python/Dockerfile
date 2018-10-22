FROM ubuntu:16.04

# Install Python 3
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-py \
    python3-pytest \
    python3-setuptools \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install -y git

RUN git clone -b master --single-branch https://github.com/Azure/azure-iot-sdk-python.git

WORKDIR /azure-iot-sdk-python

RUN git submodule update --init --recursive

WORKDIR /azure-iot-sdk-python/build_all/linux
RUN apt-get install -y sudo build-essential pkg-config libcurl3-openssl-dev git cmake libssl-dev uuid-dev libboost-python-dev

# Build for Python 3.5
RUN ./build.sh --build-python 3.5