FROM python:3.9
WORKDIR /workdir/fastapi
COPY ./requirements.txt /workdir/fastapi/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workdir/fastapi/requirements.txt
COPY ./ /workdir/fastapi
#COPY ./app /workdir/fastapi/app
RUN ls -al --recursive /workdir/fastapi
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8006"]
## CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
## above used nginx
CMD ["gunicorn"  , "--bind", "0.0.0.0:8006", "application.wsgi:app"]
