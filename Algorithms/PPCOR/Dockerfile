FROM r-base:4.0.0

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

LABEL maintainer = "Aditya Pratapa <adyprat@vt.edu>"

USER root

WORKDIR /

RUN R -e "install.packages('https://cran.r-project.org/src/contrib/ppcor_1.1.tar.gz', type = 'source')"

COPY runPPCOR.R /

RUN mkdir data/