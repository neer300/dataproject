import tweepy

from geopy import geocoders

def get_geocode_for_cities(cities):
    cities_geo = []
    for city in cities:
        georet = geoeng.geocode(city, exactly_one=False)
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


terms = 'pope twitter'
for i in range(len(cities)):
    fout = open("../resources/tweets_"+terms+"_"+cities_name[i]+".txt",'w')
    fout.write(cities_name[i]+"\n")
    fout.write(terms+"\n")
    
    geo_code  = cities[i]
    g = str(geo_code[0])+',' + str(geo_code[1]) + ',10mi'
    print "for" + cities_name[i] + ":"
    for p in range(1,8):
        for result in  api.search(q=terms,geocode=g,page=p):
            tweet  = result.text
            print tweet.encode( "utf-8" )
            fout.write(tweet.encode( "utf-8" )+"\n")
    
    fout.close();