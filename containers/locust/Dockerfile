FROM locustio/locust:1.1
#ENV PATH="/home/locust/.local/bin:${PATH}"
USER root 
RUN whoami
RUN cd ~
COPY ./dependencies.txt .
RUN pip3 install -r dependencies.txt
USER locust
RUN whoami
WORKDIR /app
COPY ./ .
RUN ls -l
# RUN python -c "import sys; print(sys.path)"


