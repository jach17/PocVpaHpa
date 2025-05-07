FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build-env
ARG NUGET_AUTH_TOKEN
ARG NUGET_USER_NAME

WORKDIR /app
COPY . ./

COPY ./nuget.config.template ./nuget.config
RUN sed -i -e "s/USER/$NUGET_USER_NAME/g" -e "s/PW/$NUGET_AUTH_TOKEN/g" nuget.config 

RUN dotnet restore "/app/Toks.Loyalty.test.Api/Toks.Loyalty.test.Api.csproj"
RUN dotnet publish "/app/Toks.Loyalty.test.Api/Toks.Loyalty.test.Api.csproj" -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine3.20
WORKDIR /app
COPY --from=build-env /app/out .

RUN apk add icu-libs --no-cache tzdata
RUN apk add libgdiplus --repository https://dl-3.alpinelinux.org/alpine/edge/testing/
RUN apk update

ENV TZ America/Mexico_City
EXPOSE 2025

ENTRYPOINT ["dotnet", "Toks.Loyalty.test.Api.dll"]
