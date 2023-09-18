FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic
# RUN python manage.py migrate
# RUN python manage.py createsuperuser --noinput \
#             --username $DJANGO_SUPERUSER_USERNAME \
#             --email $DJANGO_SUPERUSER_EMAIL \
#             --password $DJANGO_SUPERUSER_PASSWORD


CMD ["uvicorn", "clkr_core.asgi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

