FROM r-base:4.0.0
LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"
USER root

# install dependencies
RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

RUN R -e "install.packages('BiocManager')"
RUN R -e "BiocManager::install('igraph')"
RUN R -e "BiocManager::install('pcalg')"
RUN R -e "install.packages('reshape2')"
RUN R -e "install.packages('foreach')"
RUN R -e "install.packages('doParallel')"

WORKDIR /
COPY runPC.R /
RUN mkdir data/



