# Text_simiplification
Text Simplification Using a Combination of Extractive and Abstractive Approach.
Final Project For CSCI-UA 480 Natural Language Processing @ New York University
## Group Member:

* Yi (Abigale) Song
* Yilin (Elaine) Shan
* Diana Zhao
* Yuexiang (Adam) Liao

# Project Overview
This project is a text summarization system that utilizes both abstractive and extractive approaches.

# How to run the program:
## Install required packages (preferably under virtual environment)
If you want to install a virtual environment, please refer to https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ <br>
## Install tensorflow
```
pip install tensorflow
```
If you are using Apple Silicon, please refer to https://developer.apple.com/metal/tensorflow-plugin/
## Install other packages
```console
pip install nltk
pip install numpy
pip install transformer
pip install torch
pip install gensim
pip install wordfreq
```
## Get training data from the internet and download into the data folder:
```console
cd data
wget https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/complex-word-identification-dataset/cwishareddataset.zip
unzip cwishareddataset.zip
```
## Get the glove embedding model into the model folder:
```console
cd model
wget http://nlp.stanford.edu/data/glove.6B.zip
unzip glove.6B.zip -d embeddings
```
## Download the required nltk packages:
Open the python console by typing
```
python
```
Then in the python console, type:
```
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('brown')
```
## Download Stanford Core NLP
Please refer to https://stanfordnlp.github.io/CoreNLP/ for instruction.

## Launch the Stanford Core NLP server:
First go to the directory that contain the Stanford Core NLP program, then open the terminal in that directory and type:
```
java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 500
```

## Then run the program:
```consle
python src/main.py
```
