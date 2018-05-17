# CAPRI-CASP Crawlers


At the moment, the following scripts are available:

## I-TASSER Crawler

Checks the queue of the [I-TASSER server](https://zhanglab.ccmb.med.umich.edu/I-TASSER/) and downloads jobs information.

### How to use it:

For example, to download the information from the first 5 pages of the server queue:

```
python i-tasser_crawler.py 5
```
After the execution of the script, a file called i-tasser.json is generated containing for each job different information such as the email of the user, the IP address, when the job was submitted or the list of available models (if any).


## CASP models crawler

Checks the [CASP available server predictions](http://predictioncenter.org/download_area/CASP13/server_predictions/) for a given target.

### How to use it:

For example, for the T0956 target:

```
python casp-models_crawler.py T0956
```

If models for that target are found, the script will download them.