FROM python:3

RUN pip install --upgrade pip
RUN pip install chatterbot
RUN pip install websock

WORKDIR /websock

COPY . .

EXPOSE 80

CMD ["python", "./ExampleChatServer.py"]

# docker build -t chatserver .
# docker run -p 80:80 -d -v /root/WebSock/examples/chatAppServer:/websock chatserver