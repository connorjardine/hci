from flask import Flask, render_template

app = Flask(__name__)


@app.route('/map')
def hello():
    return render_template('map.html')

@app.route('/graph')
def hello():
    return render_template('graph.html')
