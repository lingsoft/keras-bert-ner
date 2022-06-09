# keras-bert-ner

Dockerized version of the Named entity recognition built on top of BERT 
and keras-bert. 

## Dependencies

### Python

Python < 3.8 and TensorFlow 1 (here cpu version is used). See 
[Issue #4](https://github.com/spyysalo/keras-bert-ner/issues/4) and
[fi-ner-eval](https://github.com/aajanki/fi-ner-eval#turku-ner).

### Model  

[Latest model](https://turkunlp.org/fin-ner.html) (combined-ext-model-130220.tar.gz) 
trained on Turku OntoNotes corpus is used.

## Quickstart

### Development

```
git clone --recurse-submodules <ADD repo>
./load-model.sh
docker build -t finbert-ner-dev -f Dockerfile.dev .
docker run -it --rm -p 8000:8000 -v $(pwd):/app -u $(id -u):$(id -g) finbert-ner-dev bash
FLASK_APP=serve.py flask run --host 0.0.0.0 --port 8000
```

Simple test call from outside of the container

```
curl -X POST localhost:8000 -d 'text=Sauli asuu Salossa'
```

### Usage

```
docker build -t finbert-ner .
docker run --rm -p 8000:8000 finbert-ner
curl -X POST localhost:8000 -d 'text=Sauli asuu Salossa'
```
