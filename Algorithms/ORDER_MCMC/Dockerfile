FROM r-base:4.0.0

LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

USER root

WORKDIR /

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

RUN R -e "install.packages('BiocManager')"
RUN R -e "BiocManager::install('graph')"
RUN R -e "BiocManager::install('RBGL')"
RUN R -e "install.packages('ggm')"
RUN R -e "BiocManager::install('Rgraphviz')"
RUN R -e "install.packages('BiDAG')"
RUN R -e "install.packages('reshape2')"
RUN R -e "install.packages('foreach')"
RUN R -e "install.packages('doParallel')"

COPY runORDER_MCMC.R /

RUN mkdir data/



