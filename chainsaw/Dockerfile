FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y git && apt install -y curl && apt install -y jq && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/WithSecureLabs/chainsaw.git /tmp/chainsaw
RUN git clone https://github.com/SigmaHQ/sigma /tmp/chainsaw/sigma
RUN curl -LJO  https://github.com/WithSecureLabs/chainsaw/releases/download/v2.9.1/chainsaw_x86_64-unknown-linux-gnu.tar.gz
RUN mkdir /tmp/chainsawbin
RUN tar xvfz chainsaw_x86_64-unknown-linux-gnu.tar.gz -C /tmp/chainsawbin
RUN chmod +x /tmp/chainsawbin/chainsaw/chainsaw
