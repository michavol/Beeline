# Benchmarking Framework for Gene Regulatory Network Inference (on Bulk Data)

This is the main repository for the Bachelor's thesis "Benchmarking Framework for Gene Regulatory Network Inference Methods", written under the supervision of Magali Champion (Add link to final document!). The thesis outlines the problem of gene regulatory network (GRN) inference, explains what kinds of data and methods exist and demonstrates how the code in this repository can be used to compare different methods for GRN inference from bulk data. It adapts and extends existing work from Pratapa et al. (2022) who focused on benchmarking methods for single-cell data (Pratapa, A., Jalihal, A.P., Law, J.N., Bharadwaj, A., Murali, T. M. (2020) "Benchmarking algorithms for gene regulatory network inference from single-cell transcriptomic data." Nature Methods, 17, 147–154.)

Their [documentation](https://murali-group.github.io/Beeline/) nicely outlines the basic structure of the framework and how it can be used. For the benchmarking framework in this repository a few modifications have been made. Here, the folder ```BashScripts``` was added, which is where ```setupAnacondaVENV.sh``` is located now. Furthermore, ```BLRunner.py``` and ```BLEvaluator.py``` and all their dependencies were adjusted to accomodate the algorithms and evaluation methods discussed in the thesis. The user for Docker Desktop is now ```18881888``` and not ```BEELINE``` - this way you can use the Docker images I used and made available on Docker Hub. As the input data used in the thesis is considerably large, I only added a few example datasets. In case you would like to have access to the complete input data that was used for the benchmarking results, please contact me. 


Quick setup:
- Setup Docker: We recommend using [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/) for Linux: 

- Setup environment: We recommend using [Anaconda](https://www.anaconda.com/) for Python. 
```
cd BashScripts
./setupAnacondaVENV.sh
conda activate grn_inference
cd ..
```

- Build Docker images - may take quite some time:
```
cd BashScripts
./initialize
cd ..
```

- Run and evaluate algorithms according to config files: (see ```BLEvaluator.py``` for meaning of arguments)
```
python BLRunner.py --config config-files/config_dream4_10.yaml
python BLEvaluator.py --config config-files/config_dream4_10.yaml -a -u -j -n -z -y -t -d -f -e -x
```

- The results can then be found in ```outputs```



