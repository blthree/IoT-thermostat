import json

import matplotlib.pyplot as pyplt

'''
'''
a = open('db.json', mode='r')
b = json.load(a)
c = b['_default']
db_array = {}
dates = []
for record in c.values():
    if record['Date'] not in db_array.keys():
        db_array[record['Date']] = []
    newrecord = {'Time': record['Time'], 'Temperature': record['Temperature']}

    db_array[record['Date']].append(newrecord)
# 2017-01-15 has 196 elements
times = []
temps = []
for record in db_array['2017-02-04']:
    no_colon = record['Time'].replace(':', '')
    times.append(int(no_colon))
    temps.append(int(record['Temperature']))
print(len(times))
print(len(temps))
pyplt.plot(times, temps, 'ro')
pyplt.axis([800, 810, 60, 72])
pyplt.show()
