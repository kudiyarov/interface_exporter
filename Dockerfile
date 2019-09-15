FROM ermescs/pyinstaller-alpine:v3.3.1-python3.6-alpine3.7 as base

LABEL maintainer="kudiyarov1994@mail.ru"
LABEL version="v0.1.0"
LABEL description="Exporter for collecting interface statuses"

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /install
COPY interface_exporter.py /install
RUN pip install -r requirements.txt && \
    pyinstaller --onefile --clean ./interface_exporter.py

FROM alpine:3.7
RUN mkdir /app
RUN addgroup -g 2000 exporter \
    && adduser -u 2000 -G exporter -s /bin/sh -D exporter
WORKDIR /app
COPY --from=base /install/dist/interface_exporter /app

USER exporter
ENTRYPOINT [ "./interface_exporter" ]