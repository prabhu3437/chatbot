# chatbot
a naive chatbot that sometimes misdiagnoses.

This retrieval-based prototype bot uses publicly available health information and a set of NLP techniques to generate indicative diagnosis and NHS leaflet for that diagnosis. The result is not to be treated as medical advice.

## Installation
Run `./install.sh`. This will create a virtual environment and install all components required within.

## Running chatbot
Within virtualenv venv (`source venv/bin/activate`), you can launch separate service:

`python3 -m chatbot.services.ask`

`python3 -m chatbot.services.symptoms`

For the first time running either service, it will take longer than usual as it needs to download, process and cache web data. Afterwards, it takes around 5 minutes to launch `ask` and instantly for `symptoms`.

## API endpoints
Following endpoints are available to consume:

`POST /chatbot/api/v1/ask`

It accepts payload as simple as `{"questions": "your questions or description of symptoms"}`


`GET /chatbot/api/v1/symptoms`
`GET /chatbot/api/v1/symptoms/<string:symptom_name>`

To list all leaflets or leaflet for the chosen symptom.

## Further ideas and development
Using vector representation of words rather than sparse matrix to extract proximity of documents;

Explore Convolutional Neural Net as text classification alternative to Naive Bayes
