from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Getting Permissions
f=InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
creds=f.run_local_server(port=0)
print(creds)
service=build("Sheets","v4", credentials=creds).spreadsheets().values()
d=service.get(spreadsheetId="1u3l2eyMCQEgUahI13YxyqSVOBPFPQSIXVHlCV_-45mM",range="B:F").execute()
data=d['values']

# Getting first 5 datapoints from dataframe
df=pd.DataFrame(data[1:], columns=data[0])
print(df.head())

mymodel=SentimentIntensityAnalyzer()
sentiment=[]
data[0].append("Sentiment")
# Getting Opinion columns only
for idx,reviews in enumerate(df.loc[:,'Opinion'],start=1):
    pred=mymodel.polarity_scores(reviews)
    if pred['compound']>=0.5:
        sentiment.append("Positive")
        data[idx].append("Positive")
    elif pred['compound']<0.5 and pred['compound']>=-0.5:
        sentiment.append("Neutral")
        data[idx].append("Neutral")
    else:
        sentiment.append("Negative")
        data[idx].append("Negative")


# Adding prediction to dataframe as sentiment feature.
df['Sentiment']=sentiment
# Saving CSV file
df.to_csv("./data/result.csv",index=False)
