FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /src
EXPOSE 8000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
