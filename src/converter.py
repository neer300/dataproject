from alchemy import AlchemyAPI
from pattern.web import Twitter, plaintext
from xml.dom.minidom import parseString
import csv
import os
import re


BASE_DIRECTORY = "./"
alchemyObj = AlchemyAPI.AlchemyAPI()
# Load the API key from disk.
keys=[]
error=0
currentKey=0

interesting_term = "kate" #'rob', 'gaza'
MAXIMUM_REQUEST_TO_ALCHEMY_PER_FILE = 75 #75
DATA_PATH = os.path.join(BASE_DIRECTORY, "data");
API_KEY_PATH = os.path.join(BASE_DIRECTORY, "resources", "api_key.txt")
CSV_FILE_PATH = os.path.join(BASE_DIRECTORY, "data", interesting_term + "_sentiment.csv")

print API_KEY_PATH
print DATA_PATH


def read_tweets(filename):
    filename = os.path.join(DATA_PATH, filename)
    print
    print "=" * 80
    print filename
    print "-" * 80
    count_positive = 0
    count_neutral = 0
    count_negative = 0
    count_ignored = 0
    sum_of_all = 0
    total_count = 0
    with open(filename, "r") as txt:
        place = txt.readline()
        term = txt.readline()
        while(total_count < MAXIMUM_REQUEST_TO_ALCHEMY_PER_FILE):
            tweet = txt.readline().rstrip()
            score = get_sentiment_from_alchemy(tweet)
            if score is not None:
                if score > 0:
                    count_positive += 1
                elif score < 0:
                    count_negative += 1
                else:
                    count_neutral += 1
                total_count += 1
                csv_row = (total_count, place, score, term, tweet)
                print csv_row
            else:
                count_ignored += 1
        
        sum_of_all = count_positive - count_negative
        sentiment_csv = (place, count_positive, count_negative, count_neutral, sum_of_all, term)
        print sentiment_csv
        csvwriter.writerow(sentiment_csv)
        

def get_sentiment_from_alchemy(tweet):
    #tweet  = tweet.encode('utf-8')
    try:
        result = alchemyObj.TextGetTextSentiment(tweet);
        dom = parseString(result);
        reflist = dom.getElementsByTagName('score');
        if len(reflist) > 0:
            score = float(reflist[0].firstChild.data);
        else:
            score = 0.0;
            
        search = re.search("(?P<url>https?://[^\s]+)", tweet)
        if search != None:
            res = search.group("url")
            result = alchemyObj.URLGetTextSentiment(res);
            dom = parseString(result);
            reflist = dom.getElementsByTagName('score');
            
            if len(reflist) > 0:
                score += float(reflist[0].firstChild.data);
            else:
                score += 0.0;
#        print str(score) + "\t" + tweet
        return score
    except:
        global error
        global currentKey
        error+=1
        print "error"
        if(error>2):
            error=0
            currentKey+=1
            currentKey %= len(keys)
            fp2=open("temp.txt",'w')
            fp2.write(keys[currentKey])
            fp2.close()
            alchemyObj.loadAPIKey("temp.txt");
        None

    
if __name__== '__main__':
    print os.getcwd()

    fp=open("./resources/api_keys.txt",'r')
    keys=fp.readlines()
    fp2=open("temp.txt",'w')
    fp2.write(keys[currentKey])
    fp2.close()
    alchemyObj.loadAPIKey("temp.txt");
    

    with open(CSV_FILE_PATH, "w+") as csvfile:
        csvwriter = csv.writer(csvfile)
        tweets_files = os.listdir(DATA_PATH)
        for filename in tweets_files:
            interesting_term = ''

            if re.search("tweets_.*\.txt", filename):
                if 'kate' in filename: 
                    interesting_term = 'kate'
                else:
                    continue
                print (interesting_term, filename)
                read_tweets(filename)