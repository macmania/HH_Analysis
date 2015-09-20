#!flask/bin/python
from flask import Flask, Response, render_template, request
from spreadsheets import get_group_dict
import json
from markov_bot import Markov
import random
import os

app = Flask(__name__)
markov_chain_ = ''
_markov_bot_ = ''
group_sentence = {}
_i = 0

hh_groups = [
    "HH: Javascript",
    "HH Computer Science",
    "HH Systems Programming",
    "HH: Music",
    "HH Hacker Problems",
    "HH Skillshare", "HH MHacks", "HH Free Stuff",
    "HH: What Are You Working On?", "HH PHP",
    "HH Job Listings", "HH Internships", "Hackathon Hackers Asia", "HH Freelance",
    "HH: Share Your Projects", "HH Ruby", "HH Throw a Hackathon", "HH Data Hackers",
    "HH Android", "HH Internet of Things", "HH Design", "HH Rust", "HH Dropouts", "HH Canada Eh?",
    "HH Coding", "HH Webdev", "HH Growthhacking", "HH Product Launch", "HH Futurism",
    "HH: Linux Users", "HH Meta", "HH Websites and Resumes", "HH Connect",
    "HH Information Security", "HH Constructive Debates",
    "HH: Code Reviews", "HH Africa", "HH Coding Interview Prep",
    "HH Sweat Equity Jobs", "HH Python", "HH iOS", "HH: Book Club",
    "HH Vim", "HH Blog Posts", "HH: VR", "HH College Apps",
    "Hackathon Hackers South East Asia (SEA)", "HH CTF", "HH Social Good",
    "HH Homework", "HH FIRST + VEX",
    "HH: Snackathon Snackers", "HH Housing", "HH Hardware Hackers"
]

# @app.route('/')
# def index():
#     return render_template('index.html')

#@app.route('/', methods=['POST'])
@app.route('/')
def get_sentences():
   # data = request.data
    #print data
    key = hh_groups[random.randint(1, len(hh_groups))]
    body = {}
    _markov_bot_ = build_markov_bot(key)
    sentences = []
    body = {
        'key': key,
        'sentences': [{}]
    }
    for i in range(10):
        sentence = _markov_bot_.generate_markov_text().decode('unicode_escape').encode('ascii','ignore')
        body['sentences'].append({
            'body': sentence
        })

    return render_template('index.html',
                           title='What would HH say?',
                           body=body)

def build_markov_bot(key):
    if len(group_sentence) == 0:
        group_sentences = get_group_dict()
    print key
    all_sentences = ' '.join(group_sentences[key])
    return Markov(all_sentences)


if __name__ == '__main__':
    app.run(debug=True)