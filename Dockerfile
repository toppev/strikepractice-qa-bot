FROM python:3.8

RUN mkdir /app
WORKDIR /app

RUN pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
ADD requirements.txt /app
RUN pip3 install -r requirements.txt

ADD . /app

CMD [ "python", "-u", "./chatbot.py" ]