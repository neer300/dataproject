import tweepy

from geopy import geocoders
import time

def get_geocode_for_cities(cities):
    cities_geo = []
    for city in cities:
        georet = geoeng.geocode(city, exactly_one=False)
        time.sleep(0.5)
        # geocode has different kinds of return values, list of tuples or a tuple.
        if type(georet) is type([]):
            place, (lat, lng) = georet[0]
        else:
            place, (lat, lng) = georet
        print (place, lat, lng)
        cities_geo.append((lat, lng))
    print cities_geo
    return cities_geo

api = tweepy.API(retry_delay=0.5)
geoeng = geocoders.Google()
cities_name = ["New York, NY, USA","Seattle, WA, USA", "San Francisco, CA, USA", "Austin, TX, USA", "Los Angeles","Madison, WI, USA","Chicago","Miami","Atlanta","Detroit"]
cities = [(40.7143528, -74.0059731), (47.6062095, -122.3320708), (37.7749295, -122.4194155), (30.267153, -97.7430608), (34.0522342, -118.2436849), (43.0730517, -89.4012302), (41.8781136, -87.6297982), (25.7889689, -80.2264393), (33.7489954, -84.3879824), (42.331427, -83.0457538)]

cities_name = ["Cairo","Tehran","Dubai","Jerusalem","Riyadh","Karachi","Baghdad","Istanbul"]
cities = [(30.0444196, 31.2357116), (35.6961111, 51.4230556), (25.271139, 55.307485), (31.768319, 35.21371), (24.7116667, 46.7241667), (24.893379, 67.0280609), (33.325, 44.422), (41.00527, 28.97696)]

cities_name += ["London","Hong Kong","Tokyo","Mumbai","Sydney","Beijing","Dublin","Paris","Rome","Madrid","Berlin","Moscow"]
cities += [(51.5073346, -0.1276831), (22.396428, 114.109497), (35.6894875, 139.6917064), (19.0759837, 72.8776559), (-33.8674869, 151.2069902), (39.90403, 116.407526), (53.3494426, -6.2600825), (48.856614, 2.3522219), (41.9015141, 12.4607737), (40.4167754, -3.7037902), (52.519171, 13.4060912), (55.7512419, 37.6184217)]
#cities = get_geocode_for_cities(cities_name)

terms = 'gaza'
for i in range(len(cities)):
    fout = open("../resources/tweets_"+terms+"_"+cities_name[i]+".txt",'w')
    fout.write(cities_name[i]+"\n")
    fout.write(terms+"\n")
    
    geo_code  = cities[i]
    g = str(geo_code[0])+',' + str(geo_code[1]) + ',10mi'
    print "for" + cities_name[i] + ":"
    for p in range(1,8):
        for result in  api.search(q=terms,geocode=g,page=p,lang='en'):
            tweet  = result.text
            print tweet.encode( "utf-8" )
            fout.write(tweet.encode( "utf-8" )+"\n")
    
    fout.close();