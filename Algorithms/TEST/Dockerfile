#FROM r-base:latest
# FROM r-base:4.2.0


# LABEL maintainer = "Michael Vollenweider <michavol@ethz.ch>"

# USER root

# WORKDIR /

# # install the dependencies of the R package located at `/portalDS`

# RUN apt-get update \
#     && apt-get install -y git \
#     && apt-get install time \
#     && apt-get install gcc-7 g++-7 gfortran-7 \
#     && R -e "install.packages("BiDAG", repos='http://cran.rstudio.com/')

# # RUN apt-get -y update -qq \ 
# #   && apt-get install -y --no-install-recommends \
# #     libgsl0-dev \ 
# #   && R -e "install.packages('BiDAG', repos='http://cran.rstudio.com/')" 
 

# COPY test.R /

# RUN mkdir data/


FROM r-base:4.0.0

RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install time

#RUN apt-get install libssl-dev

#RUN apt-get install libcurl4-openssl-dev
#/usr/lib/R/etc/Makeconf/ maybe change CXX = g++ to CXX = g++-7
#RUN apt-get install gfortran-7
#g++-7 gfortran-7


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

#RUN R -e "install.packages('https://cran.r-project.org/src/contrib/BiDAG_2.0.4.tar.gz', type = 'source')"
#RUN R -e "install.packages('https://cran.r-project.org/src/contrib/reshape2_1.4.4.tar.gz', type = 'source')"
#install.packages(c('graph', 'Rgraphviz', 'RBGL', 'pcalg'))
#RUN R -e "install.packages('reshape2',dependencies=TRUE, repos='http://cran.rstudio.com/')"
#RUN R -e "install.packages('BiDAG', repos='http://cran.rstudio.com/')" 
#dependencies=TRUE

COPY test.R /

RUN mkdir data/