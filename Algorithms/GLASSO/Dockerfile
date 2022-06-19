FROM r-base:4.0.0

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

USER root

WORKDIR /

RUN R -e "install.packages('BiocManager')"
RUN R -e "BiocManager::install('igraph')"
RUN R -e "install.packages('glasso')"
RUN R -e "install.packages('foreach')"
RUN R -e "install.packages('doParallel')"

COPY runGLASSO.R /

RUN mkdir data/



