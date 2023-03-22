from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    website = request.form['website']
    keyword = request.form['keyword']
    response = requests.get(website)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for tag in soup.find_all(True):
        if tag.name == 'a':
            href = tag.get('href')
            if keyword in href:
                results.append({
                    'tag': tag.name,
                    'text': tag.get_text(),
                    'href': href
                })
        else:
            if keyword in tag.get_text():
                results.append({
                    'tag': tag.name,
                    'text': tag.get_text(),
                    'href': None
                })
    filename = f'{website}_{keyword}_{time.time()}.json'
    with open(filename, 'w') as f:
        json.dump(results, f)
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
