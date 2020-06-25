from flask import Flask, render_template
from flask_caching import Cache
import random


app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

default = "Default"

@app.route('/')
def about():
    year = ResultService.year
    colors = ResultService.get_school_colors()
    # Import list of Andrew quips
    andrewList = []
    with open("./static/text/andrewList.txt") as f:
        for line in f:
            andrewList.append(line.strip('\n'))
    # Import list of Elijah quips
    elijahList = []
    with open("./static/text/elijahList.txt") as f:
        for line in f:
            elijahList.append(line.strip('\n'))

    andrew = random.choice(andrewList)
    elijah = random.choice(elijahList)
    order = ['men', 'women']
    if (int(year) % 2 == 0):
        order = ['women', 'men']
    return render_template("about.html", color=colors[default], year=year, order=order, andrew=andrew, elijah=elijah)

if __name__ == "__main__":
    app.run(debug = True)
