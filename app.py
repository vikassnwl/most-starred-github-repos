from flask import Flask, render_template, request
import requests, pygal

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    hist_data = ''
    if request.method == 'POST':
        lang = request.form.get('lang')
        height = request.form.get('height')
        url = 'https://api.github.com/search/repositories?q=language:'+lang+'&sort=stars'
        r = requests.get(url)
        data = r.json()
        items = data['items']
        names = []
        stars = []
        for item in items:
            names.append(item['name'])
            stars.append(item['stargazers_count'])
        hist = pygal.Bar(x_label_rotation=45, truncate_label=15, show_legend=False, height=float(height)-268)
        hist.title = 'Most-Starred '+ lang.capitalize() +' Projects on GitHub'
        hist.x_labels = names
        hist.add('', stars)
        hist_data = hist.render_data_uri()
        # hist.render_to_file('file.svg')


    return render_template('index.html', hist_data=hist_data)


if __name__ == '__main__':
    app.run(debug=True)
