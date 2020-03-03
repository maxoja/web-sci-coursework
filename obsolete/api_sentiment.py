from textblob import TextBlob

def calculate_polarity(text):
    blob = TextBlob(text)
    polarities = []
    for sentence in blob.sentences:
        polarities.append(sentence.sentiment.polarity)

    avg = (sum(polarities)/len(polarities))
    return avg

# text = '''
# The titular threat of The Blob has always struck me as the ultimate movie
# monster: an insatiably hungry, amoeba-like mass able to penetrate
# virtually any safeguard, capable of--as a doomed doctor chillingly
# describes it--"assimilating flesh on contact.
# Snide comparisons to gelatin be damned, it's a concept with the most
# devastating of potential consequences, not unlike the grey goo scenario
# proposed by technological theorists fearful of
# artificial intelligence run rampant.
# '''

# blob = TextBlob(text)
# tags = blob.tags
# noun_phrases = blob.noun_phrases

# polarities = []
# for sentence in blob.sentences:
#     # print(sentence.sentiment.polarity)
#     polarities.append(sentence.sentiment.polarity)

# avg = (sum(polarities)/len(polarities))
# print(avg)

# translated = blob.translate(to="es")
# print(translated)