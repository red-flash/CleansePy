# -*- coding: utf-8 -*-
import os
import json
import nltk
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import Series, DataFrame
from nltk import FreqDist
import matplotlib.pyplot as plt
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


#Stores variables to pass to web scrape script
#Edit these values to change video
video_id = "dxdATTOs_hc"
output_file = "YoutubeTest.json"

#Calls web scrape script
os.system(" python downloader.py --youtube "+ video_id+ " --output "+ output_file)
#method to find stored Youtube comments
def find(name, path):
    for root, firs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)




        
json_file_path = find(output_file, "C:/users/")


#Can use these lines to filter through json format
#with open(json_file_path, "r", encoding = "utf-8") as f:
    #for line in f:
        #comments = json.loads(line, encoding ="utf-8")
        #print(comments["author"])
#print(comments["author"])

#Loads delimted json into an array.
with open(json_file_path, 'r', encoding = 'utf-8') as handle:
    json_data = [json.loads(line) for line in handle]

#Can't print into IDLE because of emoji limitations.
#print(json_data)

#Create arrays to hold json data.
author = []
cid = []
text = []
time = []
vs_compound=[]
vs_pos =[]
vs_neu =[]
vs_neg =[]

#Call sentiment analysis on youtube comments and store results/info in arrays   
analyzer = SentimentIntensityAnalyzer()
for i in range(0, len(json_data)):
    author.append(json_data[i]['author'])
    cid.append(json_data[i]['cid'])
    text.append(json_data[i]['text'])
    time.append(json_data[i]['time'])
    vs_compound.append(analyzer.polarity_scores(json_data[i]['text'])['compound'])
    vs_pos.append(analyzer.polarity_scores(json_data[i]['text'])['pos'])
    vs_neu.append(analyzer.polarity_scores(json_data[i]['text'])['neu'])
    vs_neg.append(analyzer.polarity_scores(json_data[i]['text'])['neg'])

#Create Dataframe to neatly display/export information into a csv file.
youtube_df = DataFrame({'Author': author,
                        'Text': text,
                        'Compound': vs_compound,
                        'Positive': vs_pos,
                        'Neutral': vs_neu,
                        'Negative': vs_neg})
youtube_df = youtube_df[['Author','Text','Compound','Positive','Neutral','Negative']]

#youtube_df.to_csv('youtube_test.csv', encoding='utf-8', index=False)

#Optional work to find most frequent commented words
#Fdist_youtube = FreqDist(text)
#print(Fdist_youtube)
#top_10 = Fdist_youtube.most_common(9)
#stat_df = DataFrame({'Common 10 Words':top_10})
#stat_df = stat_df[['Common 10 Words']]
#stat_df.to_csv('example15.csv',encoding = 'utf-8', index=False)

#Option to use own custom profanity filter. Must name filter as custom_filter.txt
filterpath = find("custom_filter.txt", "C:/")
with open(filterpath) as f:
	content = f.read().splitlines()
#method to replace all special characters in comments.
def replace_all(text, dic):
	for i, j in dic.items():
		text = text.replace(i, j)
	return text
#Dictionary of special characters
special_char = {'@':'a', '$':'s', '0':'o', '!':'i'}

#apply special character filter to comment text
replace_text = []
for i in range(0, len(text)):
	replace_text.append(replace_all(text[i],special_char))



#Find and flag comments that are under sentiment score and contain profanity
flag_cid = []
for i in range(0, len(vs_compound)):
    if (vs_compound[i] < 0.2) or(text[i].lower() in content) or (replace_text[i].lower() in content):
        flag_cid.append(cid[i])
for i in range(0, len(flag_cid)):
    print(flag_cid[i])
        
#############################################################################
#############################Youtube Code####################################
#############################################################################
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
  print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def comments_set_moderation_status(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.comments().setModerationStatus(
    **kwargs
  ).execute()

  return print_response(response)


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()
  #"Moderate" flagged comments using channel owner's Creds.
  
  for i in range(0, len(flag_cid)):
      comments_set_moderation_status(client,
        id=flag_cid[i],
        moderationStatus='heldForReview')




