# For python files relating to index (/) page.

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

# Opens and appends to alcohol_list the list of alcohol related data
with open('static/alcohol_by_healthboard.csv') as alcohol:
    readCSV = csv.reader(alcohol, delimiter=',')
    alcohol_list = []
    for row in readCSV:
        # Just all of the potentially relevant data, can cut it down to what we need when we decide on visualisation.
        alc = {"condition": row[0], "financial year": row[4], "healthboard": row[5], "no_stays": row[11],
               "no_patients": row[13], "no_new_patients": row[15], "avg_no_stays_per_patient": row[17]}
        alcohol_list += [alc]
    # Need to delete the column header
    del alcohol_list[0]

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


def get_alcohol_by_hb(hb, year):
    for i in alcohol_list:
        if i["healthboard"] == hb and i["financial year"] == year and i["condition"] == "All alcohol conditions":
            return int(i["no_patients"])


def get_population_by_hb(hb, year):
    population = 0
    for i in pop_list:
        if i["year"] == year and i["healthboard"] == hb:
            population += int(i["count"])
    return population


# Graph of year/ratio of patients to population
def get_all_alcohol_conditions_graph(hb):
    output_list = []
    for i in range(len(financial_years)):

        if get_alcohol_by_hb(hb, financial_years[i]) is not None \
                and get_population_by_hb(hb, population_years[i]) is not None \
                and get_population_by_hb(hb, population_years[i]) is not 0:
            output_list += [[population_years[i], (get_alcohol_by_hb(hb, financial_years[i]) /
                             get_population_by_hb(hb, population_years[i])) * 100]]
    if output_list:
        return output_list


def get_hb_by_code(code):
    for i in code_list:
        if i["code"] == code:
            return i["name"]
    return "code not found"


for i in code_list:
    print(get_hb_by_code(i["code"]))
    print(get_all_alcohol_conditions_graph(i["code"]))

