# syntax=docker/dockerfile:1
FROM devo.com/ifc_base:latest

WORKDIR /devo-collector

COPY dockerfiles/.bashrc /root/.bashrc

RUN \
### Adding user LOGTRUST
    addgroup --gid 1000 logtrust &&  \
    adduser --system --shell /bin/bash --gid 1000 --uid 1000 --disabled-password logtrust &&  \
    mkdir -p /home/logtrust/ &&  \
    cp /root/.bashrc /home/logtrust/.bashrc &&  \
    chown -R logtrust:logtrust /home/logtrust &&  \
    usermod -aG sudo logtrust &&  \
    usermod -c "Logtrust main user" logtrust && \
### Adding user DEVO, password "devo"
    addgroup --gid 1001 devo &&  \
    adduser --system --shell /bin/bash --gid 1001 --uid 1001 --disabled-password devo &&  \
    mkdir -p /home/devo/ &&  \
    cp /root/.bashrc /home/devo/.bashrc &&  \
    chown -R devo:devo /home/devo &&  \
    usermod -aG sudo devo &&  \
    usermod -c "Devo main user" devo && \
###
    usermod -aG devo logtrust && \
    usermod -aG logtrust devo

RUN pip --default-timeout=10 install --upgrade pip

# Installing the DevoCollectorSDK from a local file
COPY devo-collector-sdk-1.*.tar.gz /devo-collector/
RUN ls -ltr && pip --default-timeout=10 install ./devo-collector-sdk-1.*.tar.gz && \
    rm -rf /devo-collector/devo-collector-sdk-1.*.tar.gz

ADD requirements.txt /devo-collector/
RUN pip --default-timeout=10 install -r ./requirements.txt && \
    rm -rf /devo-collector/requirements.txt

COPY agent/ /devo-collector/agent/

ENV PYTHONPATH=/devo-collector/:$PYTHONPATH

COPY metadata.json /devo-collector
RUN mkdir -p /devo-collector/config; \
    mkdir -p /devo-collector/config_internal

COPY config_internal/collector_definitions.yaml /devo-collector/config_internal/
RUN mkdir -p /devo-collector/certs; \
    mkdir -p /devo-collector/credentials; \
    mkdir -p /devo-collector/state; \
    mkdir -p /devo-collector/schemas; \
    mkdir -p /etc/devo/job; \
    mkdir -p /etc/devo/collector

COPY schemas/* /devo-collector/schemas/

#RUN chown -R devo:devo /devo-collector
#RUN chown -R devo:devo /etc/devo/
#
#USER devo

RUN date +%Y-%m-%dT%H:%M:%S.%N%z > build_time.txt

ENTRYPOINT devo-collector --config ${CONFIG_FILE:-config.yaml} --prod-mode
