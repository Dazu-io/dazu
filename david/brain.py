import json
import util
import os
from Levenshtein import distance

SIMMILARITY_ERROR_ACCEPTED = 0.3
INTENT_MODEL_FILE = './models/intent_model.json'
KNOW_FILE = './data/know.json'

def fetch_model():
    try:
        with open(INTENT_MODEL_FILE) as f:
            return json.load(f)
    except:
        return         

def persist_model(model):

    model_folder = os.path.dirname(INTENT_MODEL_FILE)
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    with open(INTENT_MODEL_FILE, 'w') as outfile:
        json.dump(model, outfile)            

def fetch_know():
    with open(KNOW_FILE) as f:
        return json.load(f)

def persist_know(data):
    with open(KNOW_FILE, 'w') as outfile:
        json.dump(data, outfile)
        
# def fetch_stopwords():
#     return set(line.strip() for line in open('./data/stopwords.txt', 'r'))

def simmilarity(a, b):
    d = distance(a, b)
    t = float(len(a) + len(b)) / 2
    if ( d/t <= SIMMILARITY_ERROR_ACCEPTED):
        return (t - d) / t
    return 0

# def persist_stopwords(data):
#     with open('./data/stopwords.json', 'w') as outfile:
#         json.dump(data, outfile)

class Brain:

    def __init__(self):
        #print("brain inited")
        self.intent_model = fetch_model()
        if self.intent_model is None:
            self.train()
        
        #self.stopwords = fetch_stopwords()

    def train(self):

        know = fetch_know()
        #self.stopwords = fetch_stopwords()

        self.intent_model = {}

        for intent, samples in know["intents"].items():
            self.intent_model[intent] = {}
            for sample in samples:
                self.intent_model[intent][sample] = {
                    "total" : 0,
                    "tokens" : {}
                }
                for t in util.tokenize(sample):
                    self.intent_model[intent][sample]["total"] += 1
                    if t in self.intent_model[intent][sample]["tokens"]:
                        self.intent_model[intent][sample]["tokens"][t] += 1
                    else:
                        self.intent_model[intent][sample]["tokens"][t] = 1

        persist_model(self.intent_model)

        return self.intent_model

    def classify(self, input):
        tokens = util.tokenize(input)
        #print ("tokens", tokens)
        intents = {}
        for intent, samples in self.intent_model.items():
            intents[intent] = 0
            for s, smeta in samples.items():
                brutal_score = 0
                stokens = smeta["tokens"]
                for t in tokens:
                    for st, value in stokens.items():
                        #print t, st, simmilarity(t, st), value
                        brutal_score += simmilarity(t, st) * value
                score = float(brutal_score) / smeta["total"]
                #print("brutal_score", s, brutal_score, smeta, intents[intent], score)        
                if intents[intent] < score:
                    intents[intent] = score
                
        intents = [{
            "intent": intent,
            "confidence": intents[intent]
        } for intent in sorted(intents, key=intents.__getitem__, reverse = True)]
        
        intents = list(filter(lambda i: i["confidence"] > 0, intents))
        
        return intents[:10]

    def nlp(self, input):
        return []