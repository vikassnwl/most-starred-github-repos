from flask import Flask, render_template, request, flash
import requests, pygal
from pygal.style import Style
import urllib.parse

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xcfNsV\x8ec\x80\x1b\xac\x07\xc0\xa0\xff\x07u\x1dow;\nY\xe2h\x9e'

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_data = ''
    if request.method == 'POST':
        lang = request.form.get('lang')
        lang_enc = urllib.parse.quote(lang) # encoded
        height = request.form.get('height')
        if lang_enc:
            url = 'https://api.github.com/search/repositories?q=language:'+lang_enc+'&sort=stars'
            r = requests.get(url)
            data = r.json()
            try:
                items = data['items']
                names = []
                plot_dicts = []
                for item in items:
                    names.append(item['name'])

                    # Get the project description, if one is available.
                    description = item['description']
                    if not description:
                        description = 'No description provided.'
                    plot_dict = {
                        'value': item['stargazers_count'],
                        'label': description[:80]+'...',
                        'xlink': item['html_url']
                    }
                    plot_dicts.append(plot_dict)

                custom_style = Style(
                    tooltip_font_size=10
                )
                chart = pygal.Bar(x_label_rotation=45, truncate_label=15, show_legend=False, height=float(height)-268, style=custom_style)
                chart.title = 'Most-Starred '+ lang.capitalize() +' Projects on GitHub'
                chart.x_labels = names
                chart.add('', plot_dicts)
                chart_data = chart.render_data_uri()
            
            except:
                flash('Invalid input')


    return render_template('index.html', chart_data=chart_data)


if __name__ == '__main__':
    app.run(debug=True)
