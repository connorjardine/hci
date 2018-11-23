from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)


@app.route('/map')
def show_map():
    if request.method == 'POST':
        # Do stuff here if needed
        return redirect(url_for('show_graph'))
    return render_template('map.html')

@app.route('/graph')
def show_graph():
    if request.method == 'POST':
        # Do stuff here if needed
        return redirect(url_for('show_map'))
    return render_template('graph.html')
