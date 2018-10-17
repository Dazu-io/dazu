import re

NON_CONTENT = r"[^\w\d\s]"
def tokenize(sentence, stopwords = []):
    #remove non content
    sentence = re.sub(NON_CONTENT, "", sentence)
    #lower
    sentence = sentence.lower();
    
    #split
    tokens = sentence.split(" ");
        
    for sw in stopwords:
        try:
            tokens.remove(sw); 
        except ValueError:
            pass        
    
    return filter(lambda t: len(t) > 0, tokens);