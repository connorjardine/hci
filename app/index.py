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
        pop = {"healthboard": row[1], "gender": row[3], "count": row[4]}
        pop_list += [pop]
    # Need to delete the column header
    del pop_list[0]




# Verified list lengths with parsed data that all is correctly parsed.
print(len(mh_list))
print(len(alcohol_list))
print(len(code_list))
print(len(pop_list))
