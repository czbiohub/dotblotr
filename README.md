# dotblotr
dotblotr is a python package for processing microarray data.

dotblotr is built upon many free open source software including (in alphabetical order):

- jupyter notebook
- matplotlib
- numpy
- pandas
- scikit-image
- scikit-learn
- scipy

## installation
To install dotblotr, first navigate to where you would like to download dotblotr and clone the repository
```
$ git clone https://github.com/czbiohub/dotblotr/
```

We recommend that you create a virtual environment. Navigate into the dotblotr directory

```
$ cd dotblotr
```
and then create a virtual environment. If you are using venv, you can do the following

```
$ python -m venv .venv
$ source .venv/bin/activate
```

If you are using anaconda, you can do the following

```
$ conda create -n dotblotr "python=3.7"
$ conda activate dotblotr
```

Finally, install dotblotr

```
$ pip install .
```

## usage
For examples of how to use dotblotr, see the notebooks in the `examples` directory.