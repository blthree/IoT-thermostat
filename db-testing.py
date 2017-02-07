import datetime
rec = {"Temperature": "71", "Time": "01:01", "Location": "BedroomTemp", "Date": "2017-01-24"}
recdate = rec['Date']
rectime = rec['Time']

print(recdt)


def makeDateObj(d, t):
    recdt = d + '.' + t
    a = datetime.datetime.strptime(recdt, '%Y-%m-%d.%H:%M')
    return a


print(a)
