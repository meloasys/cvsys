FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y \
    sudo \
    build-essential \
    git \
    ca-certificates \
    sudo \
    tzdata \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3.10-venv
    

RUN python3 -m pip install --upgrade pip

ARG user_name=cvsys
ARG user_id=1000
RUN groupadd ${user_name} -g ${user_id}
RUN useradd -lm ${user_name} -u ${user_id} -g ${user_id} -s /bin/bash
ENV USER=${user_name}
RUN echo "$user_name ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${user_name}
RUN chmod 0440 /etc/sudoers.d/${user_name}

RUN sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER ${user_name}
WORKDIR /home/${user_name}
RUN mkdir contents
WORKDIR /home/${user_name}/contents
RUN mkdir src