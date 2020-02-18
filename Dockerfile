FROM anibali/pytorch:no-cuda

WORKDIR /bots
COPY . .
COPY requirements.txt /tmp
RUN conda install git pip
RUN pip install git+https://github.com/joeynmt/joeynmt.git
RUN pip install --ignore-installed PyYAML
RUN pip install -r /tmp/requirements.txt


CMD ["python", "run.py"]
