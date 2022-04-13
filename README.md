# Detecting fake news using various machine learning techniques (and a pretty website 😇)



## Training

To get the datasets, dependencies, and code you may run

```
git clone https://github.com/y-almannaee/is-it-real
pip3 install -r requirements.txt
```

If you are running on Linux/MacOS, you must set the environment variable for NLTK_DATA to point to where the nltk data is. On Windows, this needs to be done by editing the PATH by opening System &#8594; Advanced System Settings &#8594; Environment Variables &#8594; Path &#8594; Edit 

When running on Linux, from the command line you may invoke the following command

```
NLTK_DATA="/home/USERNAME/is-it-real/.cache/nltk_data" python3 train.py
```

Trained models, corpora, processed text, etc. are stored in a .cache directory, and are not committed to this repository.

## Website backend

To be able to run on Ubuntu we need to do 

```
sudo apt install python3-pip python-dev libxml2-dev libxslt-dev
pip3 install -r requirements.txt
```