FROM locustio/locust 
#ENV PATH="/home/locust/.local/bin:${PATH}"
USER root 
RUN whoami
RUN cd ~
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
USER locust
RUN whoami
WORKDIR /app
COPY ./ .
RUN ls -l
# RUN python -c "import sys; print(sys.path)"


