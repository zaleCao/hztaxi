from flask import Flask, render_template, request, abort
from flask.ext.mongoengine import MongoEngine
from flask.views import MethodView
from mongoengine.queryset import Q


app = Flask(__name__)
#initialise DB
db = MongoEngine(app)

#configure DB
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
}

#connect to DB
db.connect('test')

#route with get request
@app.route('/')
def index():
        return render_template('map.html')

class taxis(db.Document):
	taxi_id = db.IntField()
	lng = db.FloatField()
	lat = db.FloatField()
	vel = db.FloatField()
	drt = db.FloatField()
	carry = db.IntField()
	time = db.IntField()

@app.route('/data', methods=['GET'])
def getdata():
    time = int(request.args.get('time',777)) # time as the argument of the request, defult to 737
    # set upper query limit (range of 600secs)
    time_u=time+10
    time_l=time-10
    return taxis.objects(Q(time__gte=time_l) & Q(time__lt=time_u)).to_json()
    # return taxis.objects(time=time).to_json()
    # for taxi in taxis.objects(time=time):
    	# data = json.dumps(data)
    	# return taxi.to_json()
    #.to_json()
    #print time
    #return Taxi.objects(Q(time__gte=time) & Q(time__lt=time)) #ISODate("2010-04-29T00:00:00.000Z")

# get unique taxi_ids with carry=1 in the area
@app.route('/carry', methods=['GET'])
def carry():
	time = int(request.args.get('time',777)) # time as the argument of the request, defult to 737
    # set upper query limit (range of 600secs)
    time_u=time+10
    time_l=time-10

    carry = int(request.args.get('carry',1)) 

   	lng = int(request.args.get('lng',120.169515)) 
   	lng_u = lng + 0.003
   	lng_l = lng - 0.003

   	lat = int(request.args.get('lat',30.272821))
   	lat_u = lat + 0.003
   	lat_l = lat - 0.003

    return taxis.objects(Q(carry=carry) & Q(lng__gte=lng_l) & Q(lng__lt=lng_u) & Q(lat__gte=lat_l) & Q(lat__lt=time_u) & Q(time__gte=time_l) & Q(time__lt=time_u)).to_json()

get taxi location during pickup
@app.route('/pickup', methods=['GET'])
def pickup():
    taxi_id = int(request.args.get('taxi_id',0)) # time as the argument of the request, defult to 737
    trip = int(request.args.get('trip'))
    return taxis.objects(Q(marker=1) & Q(trip=trip) & Q(taxi_id=taxi_id)).to_json()

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug = True)