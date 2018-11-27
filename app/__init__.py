from flask import Flask, request, url_for, redirect, render_template, flash
from wtforms import Form, SelectField, SubmitField
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.plotting import *

from hci.app.data import *

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "hciisbest"

currhb=0
curryr = 2011


class SimpleForm(Form):
    hb = SelectField('Languages', choices=[('0', 'NHS Ayrshire and Arran'), ('1', 'NHS Borders'),
                                           ('2', 'NHS Dumfries and Galloway'),
                                           ('3', 'NHS Fife'), ('4', 'NHS Forth Valley'), ('5', 'NHS Grampian'),
                                           ('6', 'NHS Greater Glasgow and Clyde'),
                                           ('7', 'NHS Highland'),
                                           ('8', 'NHS Lanarkshire'),
                                           ('9', 'NHS Lothian'),
                                           ('10', 'NHS Orkney'),
                                           ('11', 'NHS Shetland'),
                                           ('12', 'NHS Tayside'),
                                           ('13', 'NHS Western Isles')])


class IntermedForm(Form):
    sel = SelectField('Languages', choices=[('2011', '2011'), ('2012', '2012'), ('2013','2013'),
                                            ('2014','2014'), ('2015','2015'), ('2016','2016'), ('2017','2017')])


@app.route('/map', methods=['POST', 'GET'])
def show_map():
    form = SimpleForm(request.form)
    year = IntermedForm(request.form)

    if request.method == 'POST' and form.validate():
        print(form.hb.data)
        global currhb
        currhb= int(form.hb.data)
        return render_template('map.html', form=form, year=year)

    if request.method == 'POST' and year.validate():
        print(year.sel.data)
        global curryr
        curryr = int(year.sel.data)
        return render_template('map.html', form=form, year=year)

    return render_template('map.html', form=form, year=year)


@app.route('/graph')
def show_graph():
    if request.method == 'POST':
        # Do stuff here if needed
        return redirect(url_for('show_map'))
    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    # create a new plot with a title and axis labels

    # SAMPLE1 IS FOR ALCOHOL DATA

    sample1 = send_alcohol_data()[0][1][currhb]

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

    sample2 = return_mental_graph()[currhb]

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

