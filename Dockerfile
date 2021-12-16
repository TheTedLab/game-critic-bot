FROM python:3.8
# set work directory
WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

WORKDIR /src/test
CMD ["pytest", "-m", "parsing"]

WORKDIR /src
CMD ["python", "bot.py"]
