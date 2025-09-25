FROM python:3.13.7-alpine

WORKDIR .
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py makemigrations \
    && python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
