FROM python:3.9
WORKDIR /workdir
COPY ./requirements.txt /workdir/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /workdir/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8006"]
## CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
## above used nginx
