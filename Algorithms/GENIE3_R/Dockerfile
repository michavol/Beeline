FROM r-base:4.2.0

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

USER root

WORKDIR /

RUN R -e "install.packages('BiocManager')"
RUN R -e "BiocManager::install('GENIE3')"
RUN R -e "install.packages('doRNG')"
RUN R -e "install.packages('doParallel')"

COPY runGENIE3_R.R /

RUN mkdir data/



