#!/bin/bash
cd ..
# Building docker for the different algorithms 
echo "Building docker containers (This may take while...): "

BASEDIR=$(pwd)
USER=18881888

# You may add the -q flag (between build and -t) if you want to hide the docker build status
# cd $BASEDIR/Algorithms/ARBORETO
# docker build -t $USER/arboreto:base .
# echo "Docker container for ARBORETO is built and tagged as arboreto:base\n"

# cd $BASEDIR/Algorithms/ORDER_MCMC/
# docker build -t $USER/order_mcmc:base .
# echo "Docker container for ORDER_MCMC is built and tagged as order_mcmc:base\n"

# cd $BASEDIR/Algorithms/PARTITION_MCMC/
# docker build -t $USER/partition_mcmc:base .
# echo "Docker container for PARTITION_MCMC is built and tagged as partition_mcmc:base\n"

# cd $BASEDIR/Algorithms/PC/
# docker build -t $USER/pc:base .
# echo "Docker container for PC is built and tagged as pc:base\n"

# cd $BASEDIR/Algorithms/PIDC/
# docker build -t $USER/pidc:base .
# echo "Docker container for PIDC is built and tagged as pidc:base\n"

# cd $BASEDIR/Algorithms/PPCOR/
# docker build -t $USER/ppcor:base .
# echo "Docker container for PPCOR is built and tagged as ppcor:base\n"

cd $BASEDIR/Algorithms/GENENET/
docker build -t $USER/genenet:base .
echo "Docker container for GENENET is built and tagged as genenet:base\n"

cd $BASEDIR


