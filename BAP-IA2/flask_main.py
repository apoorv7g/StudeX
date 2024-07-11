from flask import Flask, redirect, render_template, request
import csv

app = Flask(__name__)


def get_scores():
    scores1 = []
    with open('scores.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            scores1.append({'name': row[0], 'score': int(row[1])})
    return scores1


@app.route('/')
def index():
    return redirect('/scores/1')


@app.route('/scores/<int:page>')
def scores(page):
    scores1 = get_scores()
    scores1.sort(key=lambda x: x['score'], reverse=True)
    start_index = (page - 1) * 10
    end_index = min(start_index + 10, len(scores1))
    return render_template('index.html', scores=scores1[start_index:end_index], page=page)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_text = request.form['search_text']
        scores1 = get_scores()
        search_results = [score for score in scores1 if search_text.lower() in score['name'].lower()]
        return render_template('search_results.html', search_results=search_results, search_text=search_text)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(port=9000)
