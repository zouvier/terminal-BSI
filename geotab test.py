import mygeotab

from datetime import datetime

client = mygeotab.API(username='zcisse@ample.com', password='ZCMtbF11', database='getample')
client.authenticate()



#device = client.get('FuelEvent')



devices = client.get('Trip', device='b6')


print(type(devices))
holder = []

for i in devices:
    if {'id': 'b6'} in i:
        holder.append(i)

print(holder)
#print(devices[-1])

d_duration = str(devices[20].get('drivingDuration'))






'''hours = int(d_duration[1:2])
if (int(d_duration[1:2])) != 0:
    hours = hours * 60
if int(d_duration[3:4] == 0):
    total = hours + int(d_duration[4:5])
else:
    total = hours + int(d_duration[3:5])
'''

frstmin = int(d_duration[3:5])
scndmin = int(d_duration[4:5])
hours = int(d_duration[1:2])
totalTime = []

if hours != 0:
    hours = hours * 60
    if int(d_duration[3:4] == 0):
        totalTime.append(hours + scndmin)
    else:
        totalTime.append(hours + frstmin)
elif hours == 0:
    if int(d_duration[3:4]) == 0:
        totalTime.append(scndmin + hours)
    else:
        totalTime.append(frstmin + hours)


print(totalTime[0])


