FROM python:3.12-slim

EXPOSE 5001 5001
RUN pip install python-fasthtml

ADD app/* .

CMD ["python", "main.py"]