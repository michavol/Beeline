FROM r-base:4.0.0

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

USER root

WORKDIR /

RUN R -e "install.packages('BiocManager')"
RUN R -e "BiocManager::install('graph')"
RUN R -e "BiocManager::install('RBGL')"
RUN R -e "install.packages('ggm')"
RUN R -e "BiocManager::install('Rgraphviz')"
RUN R -e "install.packages('BiDAG')"
RUN R -e "install.packages('reshape2')"

COPY runORDER_MCMC.R /

RUN mkdir data/



