import webbrowser as wb
from flask import Flask, render_template, request
import parser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getvalue():
    search_request = request.form['name']
    rt = parser.get_content(parser.get_html(search_request).text)
    text = parser.get_text(rt)
    rating = parser.relevance(text, search_request)
    answer = parser.choice_best(rating)
    wb.open(answer["link"])
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
