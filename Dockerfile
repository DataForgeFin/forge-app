FROM python:3.9 as base

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ARG APP_NAME
ENV APP_NAME=$APP_NAME
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN pip install --no-cache-dir -r requirements/prod.txt


FROM base AS ci
RUN pip install --no-cache-dir -r requirements/dev.txt
RUN make flake8 && \
    make pylint && \
    make black && \
    make pytest


FROM base AS dist
EXPOSE 8080
CMD ["make", "app"]
