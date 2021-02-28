FROM python:3.9-alpine
RUN mkdir /usr/src/app/
RUN mkdir /usr/src/app/src
ENV FLASK_APP=app.py
COPY . /usr/src/app/
WORKDIR /usr/src/app/src
RUN pip install -r ../requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
