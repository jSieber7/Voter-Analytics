# Code Repository for Visual Analytics Project

This project's primary goal is to create voter profiles using data from the General Social Survey. Two secondary objectives are to learn more about voters and to build a brand centered around voter's preferences.

In order for the code to run, you will need specific packages. The requirements are listed in a anaconda generated requirements text file. To install to a jupyter notebook accessable virtual environment you can follow the anaconda terminal prompts below:

```
# New virtual environment with packages used in the analysis
conda create --name <env name> --file requirements.txt

# Linking the virtual environment to jupyter notebook/lab
python -m ipykernel install --user --name <env name> --display-name "Python (myenv)"
```


Note: If you are going to use Juypter to look at the .ipynb files, I highly recommend installing Jupyter Lab and using the table of contents extension for easy navigation.

```
# Installing Jupyter Lab
pip install jupyterlab

# Installing the Jupyer Lab TOC extension
jupyter labextension install @jupyterlab/toc
```

