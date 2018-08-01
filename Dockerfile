FROM python:3

WORKDIR /websock

COPY . .

EXPOSE 80

CMD ["python", "./examples/ExampleChatServer.py"]