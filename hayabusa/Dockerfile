FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y git && apt install -y curl && apt install -y unzip && rm -rf /var/lib/apt/lists/*
RUN curl -LJO  https://github.com/Yamato-Security/hayabusa/releases/download/v2.16.0/hayabusa-2.16.0-all-platforms.zip
RUN mkdir /tmp/hayabusa
RUN unzip hayabusa-2.16.0-all-platforms.zip -d /tmp/hayabusa
RUN chmod +x /tmp/hayabusa/hayabusa-2.16.0-lin-x64-gnu
