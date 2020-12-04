FROM python:3.7-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir connexion[swagger-ui]

# install geni-lib
COPY geni-lib geni-lib/
WORKDIR /usr/src/app/geni-lib
RUN python3 setup.py install

# install perl scripts
WORKDIR /opt/
COPY perl/GeniResponse.pm /opt/
COPY perl/parseEmulabResponse.pl /opt/
RUN cpan JSON

WORKDIR /usr/src/app
COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["-m", "swagger_server"]