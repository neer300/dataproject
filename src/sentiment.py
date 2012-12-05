from alchemy import AlchemyAPI
from pattern.web import Twitter
from pattern.web import plaintext

import json
import re
import tweepy 

from geopy import geocoders

from xml.dom.minidom import parse,parseString

alchemyObj = AlchemyAPI.AlchemyAPI()

engine = Twitter(license=None,throttle=0.5)

api = tweepy.API(retry_delay=0.5)

# Load the API key from disk.
alchemyObj.loadAPIKey("../resources/api_key.txt");

# Geocode searching
geoeng = geocoders.Google()

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

#cities_name = ["Tehran","New York, NY, USA","Tehran","London, UK","Cairo","Hong Kong","Melbourne VIC, Australia","Sydney NSW, Australia","Seattle, WA, USA", "San Francisco, CA, USA", "Austin, TX, USA", "Los Angeles", "Dublin, Co. Dublin, Ireland", "Leeds, West Yorkshire, UK", "London, UK",  "Mumbai, Maharashtra, India", "New Delhi","Johannesburg, South Africa"]

#cities_name = ["New York, NY, USA"]
cities_name = ["New York, NY, USA","Seattle, WA, USA", "San Francisco, CA, USA", "Austin, TX, USA", "Los Angeles","Madison, WI, USA","Chicago","Miami","Atlanta","Detroit"]
#cities = [(40.713956,-74.009399), (37.788081,-122.431641),(47.576526,-122.34375),(30.268556,-97.745361),(34.052659,-118.234863)]
#cities = get_geocode_for_cities(cities_name)
cities = [(40.718119, -74.009399), (47.6062095, -122.3320708), (37.7749295, -122.4194155), (30.267153, -97.7430608), (34.0522342, -118.2436849), (43.0730517, -89.4012302), (41.8781136, -87.6297982), (25.7889689, -80.2264393), (33.7489954, -84.3879824), (42.331427, -83.0457538)]

terms = 'gaza'

#city_names=[ "NY", "Seattle", "San Francisco", "Austin", "Los Angeles", "Dublin", "Leeds", "London", "Cairo", "Mumbai", "Delhi","Johannesberg","Melbourne","Sydney","Hong Kong"]
#cities = [(35.6961111, 51.4230556),(40.713956,-74.009399), (37.788081,-122.431641),(47.576526,-122.34375),(30.268556,-97.745361),(34.052659,-118.234863),(53.347272,-6.262207),(53.807139,-1.549072),(51.508742,-0.12085),(30.107118,31.201172),(19.077693,72.877808),(28.637568,77.228394),(-26.194877,28.081055),(-37.788081,145.019531),(-33.861293,151.204834),(22.319589,114.21936)]
fout = open("../resources/tweets_gaza2.txt",'w')
fout2 = open("../resources/results_gaza2.txt",'w')

city_scores= []
for i in range(len(cities)):
    fout = open("../resources/tweets_gaza_"+cities_name[i]+".txt",'w')
#    scores = []
    geo_code  = cities[i]
    g = str(geo_code[0])+',' + str(geo_code[1]) + ',10mi'
    
#    json_obj = {}
#    json_obj["geocode"] = geo_code
#    json_obj["terms"] = terms; 
#    fout.write(cities_name[i] + ":\n"); 
    for p in range(1,31):
        for result in  api.search(q=terms,geocode=g,page=p):
            tweet  = plaintext(result.text).encode('utf-8')
            fout.write(tweet+"\n")
    
    fout.close();
#            try:
#                result = alchemyObj.TextGetTextSentiment(tweet);
#                
#                dom = parseString(result);
#                reflist = dom.getElementsByTagName('score');
#                if len(reflist) > 0:
#                    score = float(reflist[0].firstChild.data);
#                else:
#                    score = 0.0;
                    
#                search = re.search("(?P<url>https?://[^\s]+)", tweet)
#                if search != None:
#                    res = search.group("url")
#                    result = alchemyObj.URLGetTextSentiment(res);
#                    dom = parseString(result);
#                    reflist = dom.getElementsByTagName('score');
#                    
#                    if len(reflist) > 0:
#                        score += float(reflist[0].firstChild.data);
#                    else:
#                        score += 0.0;
#                        
#                scores.append(score)
#                print tweet + ":" + str(score)
#                fout.write(tweet + " : " + str(score) + "\n")
#                
#                    
#            except:
#                print "error"
#                fout.write(tweet+ "\n")
            
#    city_scores.append(scores)
#    json_obj["scores"] = scores
#    json_encoded = json.dumps(json_obj)
#    print json_encoded
#    fout2.write(json_encoded+ "\n")
    

fout.close()
fout2.close()