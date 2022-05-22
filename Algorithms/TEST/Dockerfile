FROM r-base:4.2.0

RUN apt-get update && apt-get install -y git

RUN apt-get install time

LABEL maintainer = "Aditya Pratapa <adyprat@vt.edu>"

USER root

WORKDIR /

RUN R -e "install.packages('ppcor')"

COPY test.R /

RUN mkdir data/