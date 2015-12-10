# marker.py to manipulate database
# add markers to the taxi trace data to identify different trips 
# also identifies pickup and dropoff 
from mongoengine import *

connect('test')

class taxis(DynamicDocument):
    taxi_id = IntField()
    lng = FloatField()
    lat = FloatField()
    vel = FloatField()
    drt = IntField()
    carry = IntField()
    time = IntField()
    trip = IntField()
    marker = IntField()
    meta = {'collection':'taxis'}


u_taxi_id = []

# get unique taxi_ids and append to u_taxi_id (first run to 1000)
for taxi in taxis.objects(time__lte=10):
    if (taxi.id in u_taxi_id):
    	pass
    else:
		u_taxi_id.append(taxi.taxi_id)     	


#loop through every u_taxi_id, append trip number and carry state change marker
for u in u_taxi_id:
	# initialise switch and trip to 0
	switch = 0
	trip = 0

	for x in taxis.objects(taxi_id=u):
		if (x.carry == switch):
			taxis.objects(taxi_id=u, time=x.time).update_one(marker=0)
			taxis.objects(taxi_id=u, time=x.time).update_one(trip=trip)
		else:
			switch = x.carry
			trip = trip + 1
			taxis.objects(taxi_id=u, time=x.time).update_one(marker=1)
			taxis.objects(taxi_id=u, time=x.time).update_one(trip=trip)
