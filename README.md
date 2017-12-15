# CleansePy
Please read this file first before attempting to run this project. 
This project is currently running in a proof of concept style manner. This means that it runs without any GUI or direct user input.
Future updates are planned and will be posted here first.
Please note that this project was designed with a windows environment in mind.
Libraries
---------
The following libraries need to be installed before running CleansePy:

Python 3.x
pip install pandas
pip install nltk*
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
*After installing nltk, you will need to import it into IDLE and download addition packages(Vader Sentiment).
More info on this can be found at www.nltk.org


Youtube V3 API Credentials
---------------------------
This project requires that you have obtained your api credentials and placed them in the form of a file named client_secret.json.
This step is critical if you wish to have access to moderate comments. This file must be placed into the same directory as runOther.py
Information on how to obtain credentials can be found at https://developers.google.com/youtube/registering_an_application. 

QuickStart Guide
----------------
Once you have downloaded the necesssary libraries and obtained your Youtube Data API credentials, open runOther with IDLE.
From here, you can edit whatever video you wish to scrape from by editing the video_id value found on the first line of actual code.
The video id of a particular video can be found by looking at the characters found after the v= part of a youtube video url.
Sample URL: https://www.youtube.com/watch?v=dxdATTOs_hc       Sample Video ID: dxdATTOs_hc

After scraping the comments, CleansePy will prompt you for permission to edit comments on your Youtube account. Please note that you can only edit comments on videos that your account has posted. Copy and paste the link found in the console and enter the verification code displayed in the browser. Upon successful validation, CleansePy will hold flagged comments for moderation so that you can edit them.

Custom Filtering
-----------------
You can change the dictionary based profanity filtering of CleansePy by altering the file custom_filter. At the moment, the file must be in .txt format and contain the name custom_filter.txt. the file must also be in line delimited format. Future updates will allow for a more robust filtering options.

ToDo
-------
Add GUI
Store user credentials on local machine after verification
Allow user input for channel name or video id
support for multiple dictionary file types
support for multiple operating systems
