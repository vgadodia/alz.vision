from sklearn.linear_model import LinearRegression
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
import io

import matplotlib
matplotlib.use('agg')

# print(tokenized)

def readCsv():
    thing1 = pd.read_csv("userdata.csv")
    original = (np.array([(eval(i)[0]) for i in thing1["Old Sentence"]]))
    new = (np.array([eval(i)[0] for i in thing1["New Sentence"]]))
    scores = (np.array([eval(i)[0] for i in thing1["Scores"]]))
    times = (np.array([eval(i)[0] for i in thing1["Times"]]))
    return original, new, scores, times

def process_content(original, new, scores, times):
    try:
        # for i in range(len(original)):
            # orig = sent_tokenize(original)
            # neo = sent_tokenize(new)
        cluster1 = []
        cluster2 = []
        cluster3 = []
        good = 0
        total = len(original)
        for i in range(len(original)):
            words = nltk.word_tokenize(original[i])
            tagged = nltk.pos_tag(words)
            important = []
            things_to_consider = ["NNP", "NNPS", "NN", "NNS"]
            count = 0
            while len(important) == 0 and count < len(things_to_consider):
                for word, typ in tagged:
                    hold = None
                    if typ == things_to_consider[count]:
                        hold = word
                    if hold:
                        words2 = nltk.word_tokenize(new[i])
                        for j in words2:
                            if hold == j:
                                hold = None
                                break 
                    if hold and scores[i] < 0.95:
                        important.append(hold)
                        if count == 0 or count == 1:
                            cluster1.append([hold, scores[i], times[i]])
                        # elif count == 2:
                        #     cluster2.append([hold, scores[i], times[i]])
                        # else:
                        #     cluster3.append([hold, scores[i], times[i]])
                        else: 
                            if np.random.uniform(0, 1) > 0.5:
                                cluster2.append([hold, scores[i], times[i]])
                            else:
                                cluster3.append([hold, scores[i], times[i]])
                count+=1
            if len(important) == 0:
                good+=1
                
        # print(important)
        # print(cluster1)
        # print(cluster2)
        # print(cluster3)

        return cluster1, cluster2, cluster3, good/total

    except Exception as e:
        print(str(e))


def analyse():
    orig, new, sc, time = readCsv()
    cl1, cl2, cl3, score = process_content(orig, new, sc, time)

    # print(score)

    slope = []

    figures = []

    x = np.array([k for i, j, k in cl1]).reshape(-1, 1)
    y = np.array([j for i, j, k in cl1]).reshape(-1, 1)
    plt.scatter(x, y)
    regressor = LinearRegression()
    regressor.fit(x, y)
    yval = regressor.predict(x)
    plt.title("Rate of forgetting proper nouns")
    plt.ylabel("Memory Score")
    plt.xlabel("Days")
    plt.plot(x, yval, color='red', linewidth=2)
    slope.append(regressor.coef_)
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    figures.append(pic_hash)
    # plt.show()
    plt.clf()

    x = np.array([k for i, j, k in cl2]).reshape(-1, 1)
    y = np.array([j for i, j, k in cl2]).reshape(-1, 1)
    plt.scatter(x, y)
    regressor = LinearRegression()
    regressor.fit(x, y)
    yval = regressor.predict(x)
    plt.plot(x, yval, color='red', linewidth=2)
    plt.title("Rate of forgetting nouns")
    plt.ylabel("Memory Score")
    plt.xlabel("Days")
    slope.append(regressor.coef_)
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    figures.append(pic_hash)
    # plt.show()
    plt.clf()

    x = np.array([k for i, j, k in cl3]).reshape(-1, 1)
    y = np.array([j for i, j, k in cl3]).reshape(-1, 1)
    plt.scatter(x, y)
    regressor = LinearRegression()
    regressor.fit(x, y)
    yval = regressor.predict(x)
    plt.plot(x, yval, color='red', linewidth=2)
    plt.title("Rate of forgetting nouns")
    plt.ylabel("Memory Score")
    plt.xlabel("Days")
    slope.append(regressor.coef_)
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    figures.append(pic_hash)
    # plt.show()
    plt.clf()

    descriptions = ["Proper Words", "Nouns", "Nouns"]

    # print("Your near-perfect memory score is " + str(score) +
    #     "\nNot considering your near-perfect recallations, your average rate of forgetting is " + str((sum(slope)/3)[0][0]))
    # print("You tend to forget " + descriptions[slope.index(min(slope))] +
    #     " the most, forgetting it at a rate of " + str((min(slope))[0][0]))
    
    forget_rate = str(round(((sum(slope)/3)[0][0])*100, 1))
    type_rate = "You tend to forget " + descriptions[slope.index(min(slope))] + " the most, forgetting it at a rate of " + str(round(((min(slope))[0][0])*100, 1))
    perfect_rate = "You remembered approximately " + str(round(score*100, 1))
    figures.append(perfect_rate)
    figures.append(forget_rate) 
    figures.append(type_rate)
    return figures

# print(analyse()[1])
