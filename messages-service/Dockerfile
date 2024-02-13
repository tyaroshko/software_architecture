FROM python:3.9

WORKDIR /opt/app/

COPY requirements.txt /opt/app/
RUN pip install --no-cache-dir --upgrade -r /opt/app/requirements.txt

COPY ./main.py /opt/app/

ENTRYPOINT ["uvicorn", "main:app``", "--host", "0.0.0.0", "--port", "8000", "--reload"]