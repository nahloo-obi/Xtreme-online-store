# FROM python:3.9-alpine3.13
# LABEL maintainer="nalu.com"

# ENV PYTHONBUFFERED 1

# COPY ./requirements.txt /requirements.txt
# COPY . /app
# copy ./scripts /scripts


# WORKDIR /app
# EXPOSE 8000

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     apk add --update --no-cache postgresql-client && \
#     apk add --update --no-cache --virtual .tmp-deps \
#         build-base postgresql-dev musl-dev linux-headers && \
#     /py/bin/pip install -r requirements.txt && \
#     apk del .tmp-deps && \
#     adduser --disabled-password --no-create-home app && \
#     mkdir -p /static && \
#     mkdir -p /media && \
#     mkdir -p /vol && \
#     chown -R app:app /vol /media /static && \
#     chmod -R 755 /vol /media /static && \
#     mkdir -p /app/staticfiles && \
#     chown -R app:app /app && \
#     chmod -R 755 /app && \
#     chmod -R +x /scripts

# ENV PATH="/scripts:/py/bin:$PATH"

# USER app

# CMD ["run.sh"]

FROM python:3.9-alpine3.13
LABEL maintainer="nalu.com"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . /app
copy ./scripts /scripts


WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    # mkdir -p /vol/web/static && \
    # mkdir -p /vol/web/media && \
    # chown -R app:app /vol && \
    # chmod -R 755 /vol && \
    # /py/bin/python manage.py migrate && \
    # /py/bin/python manage.py collectstatic --noinput && \
    chmod -R +x /scripts 


ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
