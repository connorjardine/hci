from flask import Flask, request, url_for, redirect, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.plotting import *
from bokeh.models import ColumnDataSource

from hci.app.data import *

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
    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    # create a new plot with a title and axis labels

    # SAMPLE1 IS FOR ALCOHOL DATA

    sample1 = send_alcohol_data()[0][1][0]

    sam1 = []
    for i in range(1, len(sample1)):
        sam1.append(sample1[i][1])

    years1 = []
    for i in range(1, len(sample1)):
        years1.append(sample1[i][0])

    left = figure(title="Number of Patients with Alcohol Related Health Conditions in " + sample1[0],
               x_axis_label='Year',
               y_axis_label='Patients', y_range=(0, 0.8))

    # add a line renderer with legend and line thickness
    left.line(years1, sam1, legend="Patients", line_width=2)

    # add a circle renderer with a size, colour and alpha
    left.circle(years1, sam1, size=10, color="navy", alpha=0.5, legend="Patients")

    # SAMPLE2 IS FOR MENTAL HEALTH DATA

    sample2 = return_mental_graph()[0]

    sam2 = []
    for i in range(1, len(sample2)):
        sam2.append(sample2[i][1])

    years2 = []
    for i in range(1, len(sample2)):
        years2.append(sample2[i][0])

    right = figure(title="Number of Patients with Mental Health Conditions in " + sample2[0],
                  x_axis_label='Year',
                  y_axis_label='Patients', y_range=(0, 0.8))

    # add a line renderer with legend and line thickness
    right.line(years2, sam2, legend="Patients", color="red", line_width=2)

    # add a circle renderer with a size, colour and alpha
    right.circle(years2, sam2, size=10, color="red", alpha=0.5, legend="Patients")

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    p = gridplot([[left, right]])

    # render template
    script, div = components(p)
    html = render_template(
        'graph.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)
