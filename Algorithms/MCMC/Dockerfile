FROM r-base:3.5.3

LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

USER root

RUN apt-get update

WORKDIR /

RUN R -e "install.packages('https://cran.r-project.org/src/contrib/BiDAG_2.0.4.tar.gz', type = 'source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/reshape2_1.4.4.tar.gz', type = 'source')"

COPY runOrderMCMC.R /

RUN mkdir data/
# && apt-get install time