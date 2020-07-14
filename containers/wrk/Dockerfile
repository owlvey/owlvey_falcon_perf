FROM skandyla/wrk
WORKDIR /app
COPY ./ .
RUN ls -l
# RUN python -c "import sys; print(sys.path)"
ENTRYPOINT ["wrk", "test", "Owlvey.Falcon.IntegrationTests.dll"] 


