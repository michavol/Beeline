FROM r-base:4.0.0

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

USER root

WORKDIR /

RUN R -e "install.packages('BiocManager')"
RUN R -e "BiocManager::install('psych')"
RUN R -e "install.packages('tmvnsim')"

COPY runCORR.R /

RUN mkdir data/



