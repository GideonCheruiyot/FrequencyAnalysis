# NLP Frequency Analysis

NLP Frequency Analysis is a web application that allows a user to upload a file and view how often the most frequent 25 words are used in it. The user can also analyse the previous ten submissions with frequency analyses data (original text, stop words setting, and resulting word frequencies).

# Overview
NLP Frequency Analysis switch between the FrequencyCount view and FrequencyAnalysis view using a navigation bar. On the FrequencyCount Tab, they can upload a file and then process it to view the 25 most frequent words with their counts, excluding stopwords. On the Frequency Analysis Tab, they can switch in between several menus displaying the ten most recent frequency analyses.Here are the page views:


## FrequencyCount Page
<img src="src/Image1.png" width="550" height ="275"><br><br>
## Word frequencies
<img src="src/Image2.png" width="550" height ="275"><br><br>

## FrequencyAnalysis Page
<img src="src/Image3.png" width="550" height ="275"><br><br>


# How to run
- First, install all the requirements needed from the requirements.txt file


```python
pip install -r requirements.txt
```

- Run:

```python
python server.py
```

- Load your browser and enter the link: 

http://127.0.0.1:5000/FrequencyCount

- You can then switch in between the tabs

:+1:  **_ _Ready!!_ to process some files**  :shipit:


## NOTE: PLEASE MAKE SURE FILES TO BE UPLOADED ARE IN THE CLONED SERVER DIRECTORY. THIS WEB APP ALLOWS UPLOAD OF TEXT FILES, EITHER USE EXAMPLES IN DIRECTORY, OR MOVE YOUR TEXT FILE TO THE DIRECTORY WITH THESE FILES THEN UPLOAD IT.

#  Libraries/frameworks you used

### Python Backend
I used Flask to write the backend for the Web App. With Flask, I used mongodb so as to be able to have persisted analysis by fetching the last N records entered into the mongodb database. To use mongodb with Python, I used Pymongo. 

### Database

mongodb with key-value relationship which was very effecient in this case. 

### Web App Frontend
I used a mix of HTML, Bootstrap, JQuery and Javascript to display the results on the frontend.

### Text Processing

I used the ntlk toolkit to tokenize the contents of the file uploaded, to find the 25 most common words and to remove stopwords when needed.

## Stemming
After normalizing the data, I used Porter's stemming algorithm based on the original paper: http://tartarus.org/martin/PorterStemmer. I simplified it since we only need to cater for two cases:

- Regularly conjugated english verbs. For example, consider "talk", "talks", "talking", and "talked" to all be forms of "talk”, and “passes”, “passed”, and “passing” to all be forms of “pass”.
- Regularly pluralized english nouns. For example, consider "cat" and "cats" to be forms of "cat".

These two cases are covered by Step 1 of Porter's algorithm implemented in server.py.



