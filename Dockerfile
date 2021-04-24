FROM python:3.8-slim-buster AS builder

WORKDIR /app

ARG SF_BUILD_COMMIT=unknown
ARG SF_BUILD_TIME=unknown

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim-buster
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . /app

ARG SF_BUILD_COMMIT=unknown
ARG SF_BUILD_TIME=unknown
LABEL swipe-food.version=$SF_BUILD_COMMIT \
      swipe-food.build-time=$SF_BUILD_TIME

ENV PATH="/opt/venv/bin:$PATH"
