FROM python:3.11

WORKDIR /
COPY ./ /

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install openssl
RUN pip install gunicorn
RUN python -c "import sys; print(sys.path)"

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]


