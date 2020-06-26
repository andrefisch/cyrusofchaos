from flask import Flask, render_template
from flask_caching import Cache
import random

app = Flask(__name__)

default = "Default"

@app.route('/')
def about():
    colors = ['3265AF', '2D385B']
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
    return render_template("about.html", color=colors, andrew=andrew, elijah=elijah)

if __name__ == "__main__":
    app.run(debug = True)
