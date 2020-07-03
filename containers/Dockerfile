FROM locustio/locust as builder
WORKDIR /build/
COPY ./ .
RUN ls -l
RUN dotnet build Owlvey.Falcon.sln -v:q
RUN dotnet publish src/Owlvey.Falcon.API -c Release -v:q
RUN ls src/Owlvey.Falcon.API/bin/Release/netcoreapp3.1

FROM locustio/locust
WORKDIR /app
COPY --from=builder /build/ . 
EXPOSE 80/tcp
ENTRYPOINT ["dotnet", "Owlvey.Falcon.API.dll"] 






