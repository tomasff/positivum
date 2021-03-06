<p align="center">
  <img src="https://raw.githubusercontent.com/tomasff/positivum/master/images/logo.png" />
</p>

<hr>

Positivum consits of a web application and a backend service which categorizes news articles by their sentiment.

**NOTE:** As of 30/06/2020 the public demo is no longer available. While the demo was run, around 34000 articles were collected and classified.
       I will release the categorized articles under an open-source license at a later time.

## How it works
Every few minutes, a background service written in Python queries different RSS feeds stored in the database and classifies them using a model.
The web application written in flask then displays the articles in the database to the users.

## Model
The model is based on BERT. I used the transformers library to create a classification model using BBC articles annotated by myself.
Currently, the dataset is quite small and this is why the sentiment analysis is not as accurate as I would like.
In the future, this could be improved by completing some of the goals mentioned below.

For documentation purposes all iterations of my training scripts were saved.

The most up-to-date model can be found below:
- [Model (tf_model.h5)](https://storage.tomasfernandes.dev/positivum/model/tf_model.h5)
- [Config (config.json)](https://storage.tomasfernandes.dev/positivum/model/config.json)

## Dependencies
The required dependencies for each component of Positivum are listed in the `requirements.txt` file inside the corresponding directory.

## Goals
- [x] Create a reasonable model which is able to classify the title of news articles as positive/neutral and negative.
- [x] Create a backend service which is able to query and store articles from different RSS feeds which are fetched from the database.
- [x] Create a web application which displays the articles stored in the database.
- [x] Improve the web application appearance.
- [x] Show a shorter page navigation when the number of pages is big.
- [ ] Use feedback from users to train and improve the model.
- [ ] Share articles feature.
- [ ] Show confidence in each sentiment on the web application.
- [ ] Release document describing the progress of this project.

## Disclaimer
This is a personal project developed for the Extend Project Qualification.
You are welcome to use this project but I will not be providing support for it.

## Dataset Source
The current dataset was annotated by myself, but is based on the following publication:

D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering", Proc. ICML 2006. [PDF](http://mlg.ucd.ie/files/publications/greene06icml.pdf) [BibTex](http://mlg.ucd.ie/files/bib/greene06icml.bib).


## License
[MIT License](https://github.com/tomasff/positivum/blob/master/LICENSE)
