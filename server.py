from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from flask import Flask, render_template, request
from werkzeug import secure_filename
from nltk.tokenize import word_tokenize
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


post = {"author": "Mike",
       "text": "My first blog post!",
       "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)


tokenizer = RegexpTokenizer(r'\w+') 
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

current_id= 30;
songs= [
             {
             "id": 1,
             "Title": "God's Plan",
             "Singer": "Drake",
             "Album": "Scorpion",
             "Genre": ["pop", "pop-rap", "trap"],
             "Summary": "“Gods Plan is a song recorded by Canadian rapper Drake, released on January 19, 2018, through Jackson, Young Money and Matthew Samuels,and Cash Money. Written by Aubrey Graham, Ronald LaTour, Daveon Noah Shebib and produced by Cardo, Yung Exclusive,  and Boi-1da, the track acts as a single from his second EP. Musically, it has been described pop as , lead singlefrom his pop-rap and trap, whose lyrics talk about fame and his fate.",
             "Label": ["Young Money", "Cash Money", "Republic"], 
             "Songwriter":["Aubrey Graham", "Ronald LaTour", "Daveon Jackson", "Matthew Samuels", "Noah Shebib"], 
             "Producer": "Boi-1da",
             "image":"https://i.redd.it/3qdoi17x5uc01.jpg"
             },

]


@app.route('/Add_item', methods=['GET', 'POST'])
def Add_item(songs=songs):
    return render_template('Add_item.html', songs=songs)


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

            from nltk.probability import FreqDist
            fdist = FreqDist(tokenized_word)

            stop_words=set(stopwords.words("english"))

            filtered_sent=[]
            for w in tokenized_word:
                if w not in stop_words:
                    filtered_sent.append(w) 
            #results
            #store results in mongo database then push to frontend

            return str(fdist.most_common(25))
 
    else:
        result = request.args.get['myfile']

    return result



if __name__ == '__main__':
   app.run(debug = True)




