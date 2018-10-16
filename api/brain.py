import json
import util

def fetch_model():
        with open('./output/intent_model.json') as f:
            return json.load(f)

def persist_model(model):
    with open('./output/intent_model.json', 'w') as outfile:
        json.dump(model, outfile);            

def fetch_know():
    with open('./input/know.json') as f:
        return json.load(f)

def persist_know(data):
    with open('./input/know.json', 'w') as outfile:
        json.dump(data, outfile);
        
def fetch_stopwords():
    return set(line.strip() for line in open('./input/stopwords.txt', 'r'))

# def persist_stopwords(data):
#     with open('./input/stopwords.json', 'w') as outfile:
#         json.dump(data, outfile);

class Brain:

    def __init__(self):
        print("brain inited")
        self.intent_model = fetch_model()
        self.stopwords = fetch_stopwords()

    def train(self):

        know = fetch_know()

        self.intent_model = {}

        for intent, samples in know["intents"].items():
            self.intent_model[intent] = {}
            for sample in samples:
                self.intent_model[intent][sample] = {
                    "total" : 0,
                    "tokens" : {}
                }
                for t in util.tokenize(sample, self.stopwords):
                    self.intent_model[intent][sample]["total"] += 1;
                    if t in self.intent_model[intent][sample]["tokens"]:
                        self.intent_model[intent][sample]["tokens"][t] += 1;
                    else:
                        self.intent_model[intent][sample]["tokens"][t] = 1;

        with open('./output/intent_model.json', 'w') as outfile:
            json.dump(self.intent_model, outfile);

        return self.intent_model; 

    def classify(self, input):
        tokens = util.tokenize(input, self.stopwords);
        #print ("tokens", tokens);
        intents = {}
        for intent, samples in self.intent_model.items():
            intents[intent] = 0
            for s, smeta in samples.items():
                brutal_score = 0
                stokens = smeta["tokens"]
                for t in tokens:
                    if t in stokens:
                        brutal_score += stokens[t]
                score = float(brutal_score) / smeta["total"]
                #print("brutal_score", s, brutal_score, smeta["total"], intents[intent], score)        
                if intents[intent] < score:
                    intents[intent] = score
                
        intents = [{
            "intent": intent,
            "confidence": intents[intent]
        } for intent in sorted(intents, key=intents.__getitem__, reverse = True)]
        
        intents = list(filter(lambda i: i["confidence"] > 0, intents))
        
        return intents[:10]; 

    def nlp(self, input):
        return [];      