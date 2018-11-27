from bokeh.plotting import figure, output_file, show

import csv

# Opens and appends to code_list the list of healthboards and their relevant code
with open('static/codes_healthboard.csv') as codes:
    readCSV = csv.reader(codes, delimiter=',')
    code_list = []
    for row in readCSV:
        hbc = {"code": row[0], "name": row[2]}
        code_list += [hbc]
    # Need to delete the column header
    del code_list[0]

# Opens and appends to mh_list the list of psychiatric inpatient activity data
with open('static/mentalhealth_by_healthboard.csv') as mh:
    readCSV = csv.reader(mh, delimiter=',')
    mh_list = []
    for row in readCSV:
        # Just all of the potentially relevant data, can cut it down to what we need when we decide on visualisation.
        mhs = {"financial year": row[0], "healthboard": row[1], "no_admissions": row[2],
               "no_discharges": row[3], "no_stays": row[4], "no_patients": row[5], "no_hospital_residents": row[6]}
        mh_list += [mhs]
    # Need to delete the column header
    del mh_list[0]

# Opens and appends to pop_list the list of populations for each healthboard
with open('static/population_healthboard.csv') as pop:
    readCSV = csv.reader(pop, delimiter=',')
    pop_list = []
    for row in readCSV:
        # Just all of the potentially relevant data, can cut it down to what we need when we decide on visualisation.
        pop = {"year": row[0], "healthboard": row[1], "gender": row[3], "count": row[4]}
        pop_list += [pop]
    # Need to delete the column header
    del pop_list[0]

financial_years = ["2006,07", "2007,08", "2008,09", "2009,10", "2010/11", "2011/12",
                   "2012/13", "2013/14", "2014/15", "2015/16", "2016/17"]

population_years = ["2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]


# Function to obtain the population by healthboard and year
def get_population_by_hb(hb, year):
    population = 0
    for i in pop_list:
        if i["year"] == year and i["healthboard"] == hb:
            population += int(i["count"])
    return int(population)


# Function to obtain the number of mental health related patients by healthboard and year
def get_mental_by_hb(hb, year):
    for i in mh_list:
        if i["healthboard"] == hb and i["financial year"] == year:
            return int(i["no_patients"])


# Graph of year/ratio of patients to population for mental health
def get_mental_graph(hb):
    output_list = []
    for i in range(len(financial_years)):

        if get_mental_by_hb(hb, financial_years[i]) is not None \
                and get_population_by_hb(hb, population_years[i]) is not None \
                and get_population_by_hb(hb, population_years[i]) is not 0:
#            output_list += [[population_years[i], float(get_mental_by_hb(hb, financial_years[i]) /
#                             get_population_by_hb(hb, population_years[i])) * 100]]
            output_list += [[population_years[i], float(get_mental_by_hb(hb, financial_years[i]))]]
    if output_list:
        return output_list


# Function to obtain the healthboard from the code
def get_hb_by_code(code):
    for i in code_list:
        if i["code"] == code:
            return i["name"]
    return "code not found"


# Returns the data for graphing each healthboard's mental health patients by year
def return_mental_graph():
    otg = []
    for i in code_list:
        if get_mental_graph(i["code"]) is not None:
            temp = [get_hb_by_code(i["code"])] + get_mental_graph(i["code"])
            otg += [temp]
    return otg


# edit this to get a different healthboard
sample = return_mental_graph()[3]
print(sample)

sam = []
for i in range(1, len(sample)):
    sam.append(sample[i][1])
print(sam)

years = []
for i in range(1, len(sample)):
    years.append(sample[i][0])
print(years)

# prepare some data
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title="Number of Patients with Mental Health Conditions in " + sample[0],
           x_axis_label='Year',
           y_axis_label='Patients')

# add a line renderer with legend and line thickness
p.line(years, sam, legend="Patients", line_width=2)

# show the results
show(p)