'''

playing with the ASB and Crime data

@author: ignacioelola

date: 2014-02-15

'''
import sys
import csv
import json
import datetime

import math
 
 
def great_circle_distance(lat1, lon1, lat2, lon2):
	EARTH_RADIUS = 6378137  

	dLat = math.radians(lat2 - lat1)
	dLon = math.radians(lon2 - lon1)
	a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
		math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
		math.sin(dLon / 2) * math.sin(dLon / 2))
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	d = EARTH_RADIUS * c

	return d


police_crime={}

i=0
with open("policecrimedata.json","rb") as fp:
	for line in fp:
		police_crime[i]=json.loads(line)
		i=i+1

#print json.dumps(police_crime,indent=4)

print "About the police crime data:"
print "number of records: %s" % len(police_crime)

crimes_cat=[]
longitudes=[]
latitudes=[]
street_names=[]
context=[]
for record in police_crime:
	#print json.dumps(police_crime[record],indent=4)
	crimes_cat.append(police_crime[record]["crime_category"])
	longitudes.append(float(police_crime[record]["longitude"]))
	latitudes.append(float(police_crime[record]["latitude"]))
	street_names.append(police_crime[record]["street_name"])
	#context.append(police_crime[record]["context"])
	#print datetime.datetime.fromtimestamp((police_crime[record]["entryTimeStamp"]["$date"]/1000))
	#print police_crime[record]["month"]
	#sys.exit()

possible_crime_cat=set(crimes_cat)
print "\nThere are %s crime categories:" % len(possible_crime_cat)
for cat in possible_crime_cat:
	print "%s: %s %%" % (cat,(100*float(crimes_cat.count(cat))/len(crimes_cat)))
print "\nAll timestamps of the crimes are from 2013-12-01"

event_date_cleansing=[]
street_names_cleansing=[]
lat_cleansing=[]
long_cleansing=[]
vomit=[]
human_fouling=[]
blood=[]
urine=[]
with open("WCC_CleansingAntiSocialBehaviour.csv","rb") as infile:
	reader = csv.reader(infile)
	for row in reader:
		if row[2]!=str(0) and row[3]!=str(0):
			try:
				lat_cleansing.append(float(row[2]))
				long_cleansing.append(float(row[3]))
			except:
				lat_cleansing.append("")
				long_cleansing.append("")
			try:
				event_date_cleansing.append(datetime.datetime(int(row[0][0:4]),int(row[0][5:7]),int(row[0][8:10])))
			except:
				event_date_cleansing.append("")
			street_names_cleansing.append(row[1])
			vomit.append(row[6])
			human_fouling.append(row[7])
			blood.append(row[8])
			urine.append(row[9])

event_date_cleansing=event_date_cleansing[1:]
street_names_cleansing=street_names_cleansing[1:]
lat_cleansing=lat_cleansing[1:]
long_cleansing=long_cleansing[1:]
vomit=vomit[1:]
human_fouling=human_fouling[1:]
blood=blood[1:]
urine=urine[1:]

print "\nThere are %s Cleansing events between %s and %s" % (len(event_date_cleansing),min(event_date_cleansing),max(event_date_cleansing))
print "From which %s %% are vomit events" % (100*float(vomit.count("Yes"))/len(event_date_cleansing))
print "From which %s %% are human fouling events" % (100*float(human_fouling.count("Yes"))/len(event_date_cleansing))
print "From which %s %% are blood events" % (100*float(blood.count("Yes"))/len(event_date_cleansing))
print "From which %s %% are urine events" % (100*float(urine.count("Yes"))/len(event_date_cleansing))

#Can I use all cleansing data or only the one of december 2013? How many data are on that month?
count_events=0
for dtime in event_date_cleansing:
	if dtime.year==2013 and dtime.month==12:
		count_events=count_events+1
print "Only %s cleansing events were on 2013-12" % count_events

#take a lookf to lat and long in bot datasets
print "Lat for crimes between %s and %s, for cleansing %s and %s " % (min(latitudes),max(latitudes),min(lat_cleansing),max(lat_cleansing))
print "Long for crimes between %s and %s, for cleansing %s and %s " % (min(longitudes),max(longitudes),min(long_cleansing),max(long_cleansing))

all_distances=[]
for i in range(0,len(latitudes)):
	for j in range(0,len(lat_cleansing)):
		all_distances.append(great_circle_distance(latitudes[i],longitudes[i],lat_cleansing[j],long_cleansing[j])/1000)

print max(all_distances)
print min(all_distances)
