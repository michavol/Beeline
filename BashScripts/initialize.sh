#!/bin/bash
cd ..
# Building docker for the different algorithms 
echo "Building docker containers (This may take while...): "

BASEDIR=$(pwd)
USER=18881888

#You may add the -q flag (between build and -t) if you want to hide the docker build status
cd $BASEDIR/Algorithms/ARBORETO
docker build -t $USER/arboreto:base .
echo "Docker container for ARBORETO is built and tagged as arboreto:base\n"

cd $BASEDIR/Algorithms/ORDER_MCMC/
docker build -t $USER/order_mcmc:base .
echo "Docker container for ORDER_MCMC is built and tagged as order_mcmc:base\n"

cd $BASEDIR/Algorithms/PARTITION_MCMC/
docker build -t $USER/partition_mcmc:base .
echo "Docker container for PARTITION_MCMC is built and tagged as partition_mcmc:base\n"

cd $BASEDIR/Algorithms/PC/
docker build -t $USER/pc:base .
echo "Docker container for PC is built and tagged as pc:base\n"

# cd $BASEDIR/Algorithms/GLASSO/
# docker build -t $USER/glasso:base .
# echo "Docker container for GLASSO is built and tagged as glasso:base\n"

# cd $BASEDIR/Algorithms/PIDC/
# docker build -t $USER/pidc:base .
# echo "Docker container for PIDC is built and tagged as pidc:base\n"

# cd $BASEDIR/Algorithms/PPCOR/
# docker build -t $USER/ppcor:base .
# echo "Docker container for PPCOR is built and tagged as ppcor:base\n"

# cd $BASEDIR/Algorithms/GENENET/
# docker build -t $USER/genenet:base .
# echo "Docker container for GENENET is built and tagged as genenet:base\n"

# cd $BASEDIR/Algorithms/ARACNE/
# docker build -t $USER/aracne:base .
# echo "Docker container for ARACNE is built and tagged as aracne:base\n"

# cd $BASEDIR/Algorithms/CORR/
# docker build -t $USER/corr:base .
# echo "Docker container for CORR is built and tagged as corr:base\n"

# cd $BASEDIR/Algorithms/GENIE3_R/
# docker build -t $USER/genie3_r:base .
# echo "Docker container for GENIE3_R is built and tagged as genie3_r:base\n"

cd $BASEDIR


