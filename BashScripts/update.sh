### Script for updating forked repository

#git remote add upstream git@github.com:michavol/benchmarking_GRN_inference.git
cd ..

git fetch --all
git merge upstream/master
