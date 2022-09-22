FROM yamamon/centos7-minimal:latest
# RUN yum update -y
RUN yum install python3 -y
RUN mkdir /root/app
COPY . /root/app
WORKDIR /root/app
COPY . /root/app 
RUN  pip3 install  -r requirement_pip.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]
