FROM python:3.7-slim-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py /app/
#ENTRYPOINT ["python"]
ENV AWS_REGION ${AWS_REGION:-us-east-1}
CMD ["python", "generate_template.py"]
