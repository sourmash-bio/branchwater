

```
mkdir -p bw_k21
cd bw_k21

pixi exec wget -c --recursive --no-parent -nH --cut-dirs=3 --reject "index.html*" https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-k21-s100000/ -P index/

cargo run --release -p branchwater-index metadata index -o manifest && \
tail +3 manifest|cut -d, -f1 | cut -d/ -f2|cut -d. -f1 > sraids
```
