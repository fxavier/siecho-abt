FROM python:3.9-alpine3.13

LABEL maintainer="xavierfrancisco353@gmail.com"

ENV PYTHONUNBUFFERED 1

# Copying requirements first to leverage Docker cache
COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app

EXPOSE 8000

# Install dependencies in a single RUN command to reduce layers
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache \
      postgresql-client \
      gcc \
      libc-dev \
      make \
      git \
      libffi-dev \
      openssl-dev \
      python3-dev \
      libxml2-dev \
      libxslt-dev \
      build-base \
      postgresql-dev \
      musl-dev \
      linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home app && \
    # Clearing APK cache
    rm -rf /var/cache/apk/*

# Setting up application directories
RUN mkdir -p /vol/web/static /vol/web/media && \
    chown -R app:app /vol /app && \
    chmod -R 755 /vol/web && \
    chmod -R 777 /py/*

ENV PATH="/py/bin:$PATH"

USER app

# Changing CMD to an entrypoint script that can handle migrations
# Create an entrypoint.sh script in your project that runs migrations before starting the server
# COPY ./entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

 CMD ["run.sh"]