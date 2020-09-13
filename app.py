from flask import Flask, render_template, request, flash
import requests, pygal

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xcfNsV\x8ec\x80\x1b\xac\x07\xc0\xa0\xff\x07u\x1dow;\nY\xe2h\x9e'

@app.route('/', methods=['GET', 'POST'])
def index():
    hist_data = ''
    if request.method == 'POST':
        lang = request.form.get('lang')
        height = request.form.get('height')
        url = 'https://api.github.com/search/repositories?q=language:'+lang+'&sort=stars'
        r = requests.get(url)
        data = r.json()
        try:
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
        
        except:
            flash('Invalid input')


    return render_template('index.html', hist_data=hist_data)


if __name__ == '__main__':
    app.run(debug=True)
