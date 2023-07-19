FROM python:3.10

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080

CMD ["sh", "-c", "python ./app.py"]