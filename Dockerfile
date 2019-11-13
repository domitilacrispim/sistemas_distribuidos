FROM python:3.7
WORKDIR /home/graduacao/sistemas_distribuidos-master/src/
COPY ./ /home/graduacao/sistemas_distribuidos-master/src/
RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install bcrypt
EXPOSE 5002
CMD ["python3.7", "server.py", "2"]


