import random
from settings import setting
from get_urls import web_pages
from textmining import NHSTextMiner, NLPProcessor
import time
import pip

__author__ = 'Ming Li'


def install(package):
    """dynamically install missing package"""
    pip.main(['install', package])


try:
    from nltk.tokenize import word_tokenize
    from nltk.classify import NaiveBayesClassifier
    import nltk
except ImportError:
    install('nltk')
    from nltk.tokenize import word_tokenize
    from nltk.classify import NaiveBayesClassifier
    import nltk


# nltk.download('punkt')
nlp_processor = NLPProcessor()

web_scraper = NHSTextMiner(urls=list(set(web_pages.values())), attrs=setting, display=True)
data = web_scraper.extract()
labels = {key: data[key][0] for key in data}
# cleansed_data = {key: web_scraper.cleanse(data[key]) for key in data}
processed_data = nlp_processor.process(data, {'pos': True, 'stop': True, 'lemma': True})

# miner extracts subject, meta content (e.g. description of the page), main article


def generate_training_set(data, n=200, sample_size=50):

    feature_set = list()
    for key in data:
        words = word_tokenize(data[key])
        row = [tuple((web_scraper.word_feat(random.sample(words, sample_size)), labels[key])) for repeat in range(n)]
        feature_set += row

    return feature_set

feature_set = generate_training_set(processed_data)
mapping = {v: k for k, v in labels.items()}

clf = NaiveBayesClassifier.train(feature_set)


def decorator_converse(func):

    def t():
        time.sleep(2)
        pass

    def wrapper():

        while True:

            question = input('\nhow can I help you?')

            if len(question) == 0:
                break

            output = func(classifier=clf, question=question)

            if output and output[1] == 0:
                t()
                print('\nBased on what you told me, here is my diagnosis: {0}.'.format(output[0]))
                t()
                q = input('\nwould you like to have NHS leaflet?')
                if 'yes' in q.lower():
                    print('here is the link: {0}'.format(mapping[output[0]]))
                #
                # q = input('\nwould you like to ask more questions?')
                # if 'yes' in q.lower():
                #     continue
                # else:
                #     break
            elif not output:
                t()
                print('\nSorry I don\'t have enough knowledge to help you, you can improve result by asking more specific questions')
                continue
            else:
                t()
                print('\nBased on what you told me, here are several possible reasons, including: \n\n{0}'.\
                      format(output), '\n\nYou can improve result by asking more specific questions')
                # t()
                # q = input('\nwould you like to ask more questions?')
                # if 'yes' in q.lower():
                #     continue
                # else:
                #     break

    return wrapper


@decorator_converse
def main(classifier, question, decision_boundary=.9, limit=5, settings={'pos': True, 'stop': True, 'lemma': True}):

    options = list()
    words = web_scraper.word_feat(word_tokenize(nlp_processor.process(question, settings)))
    print('understanding {}...'.format(words))
    obj = classifier.prob_classify(words)
    keys = list(obj.samples())

    for key in keys:

        prob = obj.prob(key)
        options.append((key, prob))

    options.sort(key=lambda x: x[1], reverse=True)
    options = options[:limit]

    if options[0][1] > decision_boundary:
        return obj.max(), 0
    elif options[0][1] > decision_boundary / 3:
        return ';\n'.join([pair[0] + ': ({:.0%})'.format(pair[1]) for pair in options])
    else:
        return None

if __name__ == '__main__':
    main()
