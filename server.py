from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from flask import Flask, render_template, request
from werkzeug import secure_filename
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import pymongo
import os
import datetime


#Loading NLTK

import nltk
from nltk import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# initialize connection to MongoDB and retrieve access to data files

client = pymongo.MongoClient("mongodb://Bedoki:Bedoki12@cluster0-shard-00-00-p63uk.gcp.mongodb.net:27017,cluster0-shard-00-01-p63uk.gcp.mongodb.net:27017,cluster0-shard-00-02-p63uk.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.HumanPractice

collection = db.Freq

tokenizer = RegexpTokenizer(r'\w+') 
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = Stemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word,0,len(word)-1)
        stems.append(stem)
    return stems

@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':
        # for secure filenames. Read the documentation.
        file = request.files['myfile']
        filename = secure_filename(file.filename) 

        with open(filename) as f:
        #with open("/Users/mercytich/Desktop/filename") as f:
            file_content = f.read()  
            tokenized_word=word_tokenize(file_content)   
            tokenized_word = [word for word in tokenized_word if word.isalpha()]
            print(tokenized_word)
            token_word = stem_words(tokenized_word)
            print(token_word)
            

            stop_words=set(stopwords.words("english"))

            fdist_withStopwords = FreqDist(tokenized_word)
            with_Stopwords_25 = fdist_withStopwords.most_common(25)
            
            filtered_word=[]
            for w in tokenized_word:
                if w not in stop_words:
                    filtered_word.append(w) 

            fdist_withoutStopwords = FreqDist(filtered_word)
            without_Stopwords_25 = fdist_withoutStopwords.most_common(25)

            #add  (original text, stop words setting, and resulting word frequencies) to the mongodb collection
            stopwords_flag= "No_Stopwords"
            is_checked = request.form.get('option_1')
            if(is_checked=='on'):
                stopwords_flag= "No_Stopwords"
                without_stopwords_data = {
                        'original_text': file_content,
                        'stop_words_setting': stopwords_flag,
                        'word_frequencies': without_Stopwords_25
                    }
                result = collection.insert_one(without_stopwords_data)       

            else:
            #with stopwords
                stopwords_flag = "Stopwords"
                stopwords_data = {
                        'original_text': file_content,
                        'stop_words_setting': stopwords_flag,
                        'word_frequencies': with_Stopwords_25
                    }

                result = collection.insert_one(stopwords_data)
                

            #store results in mongo database then push to frontend
            return render_template('Add_item.html', results=without_Stopwords_25) 



@app.route('/FrequencyCount', methods=['GET', 'POST'])
def FrequencyCount():         
    return render_template('Add_item.html')

#fetch analysis from mongod database
@app.route('/FrequencyAnalysis', methods=['GET','POST'])
def FrequencyAnalysis():
    #query to pull the most recent 11 items from mongo database
    myresult = collection.find().skip(collection.count() - 11)
    list   = []
    for i in myresult:
        list.append(i)
 
    
    return render_template('analysis.html', list = list)

#Implemented Porter Stemmer that only does Step 1 based on the instructions given.
#In Porter Stemmer, Step1 deals with plurals and past participles

class Stemmer:
    def __init__(self):

        self.str = ""
        self.x = 0
        self.x_begin = 0
        self.z = 0   

    def consonant(self, i):
        if self.str[i] == 'a' or self.str[i] == 'e' or self.str[i] == 'i' or self.str[i] == 'o' or self.str[i] == 'u':
            return False
        if self.str[i] == 'y':
            if i == self.x_begin:
                return True
            else:
                return (not self.consonant(i - 1))
        return True

    # *o        -       the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
    def cvc(self, i):
        if i < (self.x_begin + 2) or not self.consonant(i) or self.consonant(i-1) or not self.consonant(i-2):
            return False
        ch = self.str[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return False
        return True


# *S        -       the stem ends with S (and similarly for the other letts).
    def endswith(self, s):

        size = len(s)
        if s[size - 1] != self.str[self.x]: # tiny speed-up
            return False
        if size > (self.x - self.x_begin + 1):
            return False
        if self.str[self.x-size+1:self.x+1] != s:
            return False
        self.z = self.x - size
        return True

    def set(self, s):
        size = len(s)
        self.str = self.str[:self.z+1] + s + self.str[self.z+size+1:]
        self.x = self.z + size


    def M(self):
        n = 0
        i = self.x_begin
        while 1:
            if i > self.z:
                return n
            if not self.consonant(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.z:
                    return n
                if self.consonant(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.z:
                    return n
                if not self.consonant(i):
                    break
                i = i + 1
            i = i + 1
# *v*       -       the stem contains a vowel.
    def hasVowel(self):
        for i in range(self.x_begin, self.z + 1):
            if not self.consonant(i):
                return True
        return False

# *d        -       the stem endswith with a double consonant (e.g. -TT, -SS).
    def doubleconsonant(self, j):
        if j < (self.x_begin + 1):
            return False
        if (self.str[j] != self.str[j-1]):
            return False
        return self.consonant(j)

#In Porter Stemmer, Step1 deals with plurals and past participles

    def step1(self):
        if self.str[self.x] == 's':
            if self.endswith("sses"):
                self.x = self.x - 2
            elif self.endswith("ies"):
                self.set("i")
            elif self.str[self.x - 1] != 's':
                self.x = self.x - 1
        if self.endswith("eed"):
            if self.M() > 0:
                self.x = self.x - 1
        elif (self.endswith("ed") or self.endswith("ing")) and self.hasVowel():
            self.x = self.z
            if self.endswith("at"):   self.set("ate")
            elif self.endswith("bl"): self.set("ble")
            elif self.endswith("iz"): self.set("ize")
            elif self.doubleconsonant(self.x):
                self.x = self.x - 1
                ch = self.str[self.x]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.x = self.x + 1
            elif (self.M() == 1 and self.cvc(self.x)):
                self.set("e")


    def stem(self, p, i, j):
        self.str = p  
        self.x = j
        self.x_begin = i
        if self.x <= self.x_begin + 1:
            return self.str
        self.step1()
        return self.str[self.x_begin:self.x+1]

if __name__ == '__main__':
   app.run(debug = True)




