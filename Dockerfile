FROM python:3.6.5

COPY scripts/ /bots/scripts
COPY transformer/ /bots/transformer
COPY joey_mnt_scripts /bots/joey_mnt_scripts
COPY .env /bots/env
COPY config.py /bots/config.py
COPY run.py /bots/run.py
COPY requirements.txt /tmp
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip3 install git+https://github.com/joeynmt/joeynmt.git
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python", "run.py"]
