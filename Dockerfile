FROM python:3.6-alpine

FROM 0

RUN mkdir /install
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM 0

COPY --from=1 /install /usr/local
COPY . /app
RUN apk --no-cache add libpq
WORKDIR /app
EXPOSE 5000
CMD ["python", "app/interface.py"]
