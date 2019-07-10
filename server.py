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

            fdist_withStopwords = FreqDist(tokenized_word)
            fdist_withoutStopwords = FreqDist(tokenized_word)

            #add  (original text, stop words setting, and resulting word frequencies) to the mongodb collection
            stopwords_flag= "False"
            is_checked = request.form.get('option_1')
            if(is_checked!='on'):

                stopwords_flag= "False"
                with_Stopwords_25 = fdist_withStopwords.most_common(25)
                json_without_stopwords = {
                        'title': 'Learning Python',
                        'content': 'Learn Python, it is easy',
                        'author': 'Bill'
                    }

            else:

                stopwords_flag = "True"
                stop_words=set(stopwords.words("english"))
            #without stopwords
                filtered_word=[]
                for w in tokenized_word:
                    if w not in stop_words:
                        filtered_word.append(w) 
                fdist_withoutStopwords = FreqDist(filtered_word)
                without_Stopwords_25 = fdist_withoutStopwords.most_common(25)

                json_stopwords = {
                        'title': 'Learning Python',
                        'content': 'No',
                        'author': 'Bill'
                    }


            #store results in mongo database then push to frontend
            return render_template('Add_item.html', results=fdist_withoutStopwords.most_common(25))

    else:

        result = request.args.get(['myfile'])


    return result



@app.route('/FrequencyCount', methods=['GET', 'POST'])
def FrequencyCount():          
    return render_template('Add_item.html')

#fetch analysis from mongod database
@app.route('/Analysis', methods=['GET','POST'])
def Analysis_WithoutStopWords():
    return render_template('stopwords.html')



if __name__ == '__main__':
   app.run(debug = True)




