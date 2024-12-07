from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit as st
import plotly.express as px

st.set_page_config("Amazon Review Sentiment Analysis System",page_icon='https://static.vecteezy.com/system/resources/previews/026/226/868/non_2x/sentiment-analysis-icon-illustration-vector.jpg')
st.title("AMAZON REVIEW SENTIMENT ANALYSIS SYSTEM")
choice=st.sidebar.selectbox("MY MENU",("HOME", "ANALYSIS", "RESULT"))

if choice=="HOME":
    st.image("https://camo.githubusercontent.com/af6d1852b5fad2894cacc29678363df035d3c6005a3364ac33cb5181b6b65d7f/68747470733a2f2f696d657269742e6e65742f77702d636f6e74656e742f75706c6f6164732f323032312f30372f776861742d69732d73656e74696d656e742d616e616c797369732e6a7067",
    width=600)
    st.write("1.	It is a Natural Language Processing application which can analyze the sentiment on the amazon customer review text data.")
    st.write("""2.	This application predicts the sentiment into 3 categories:\n
    a.	Positive\n
    b.	Negative\n
    c.	Neutral
            """)
    st.write("3.	This application can get the data through a google sheet.")


elif choice=="ANALYSIS":
    sid=st.text_input("Enter your Google sheet ID")
    r=st.text_input("Enter the range between first and the last column")
    c=st.text_input("Enter the text column that is to analyzed")
    btn=st.button("Analyze")

    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('key.json',["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state['cred']=f.run_local_server(port=0)
        mymodel=SentimentIntensityAnalyzer()
        service=build("Sheets","v4",credentials=st.session_state['cred']).spreadsheets().values()
        k=service.get(spreadsheetId=sid,range=r).execute()
        d=k['values']

        df=pd.DataFrame(d[1:],columns=d[0])
        l=[]
        for i in range(df.shape[0]):
            t=df._get_value(i,c)
            pred=mymodel.polarity_scores(t)

            if pred["compound"]>0.5:
                l.append("Positive")
            elif pred['compound']<0.5 and pred['compound']>-0.5:
                l.append("Neutral")
            else:
                l.append("Negative")

        df['Sentiment']=l
        df.to_csv("./data/result.csv",index=False)
        st.subheader("The result is saved as \"result.csv\" successfully.")


else:
    df=pd.read_csv("./data/result.csv")
    choice2=st.sidebar.selectbox("Choose Visualization",("NONE","PIE CHART", "HISTOGRAM", "SCATTERPLOT"))
    st.dataframe(df)
    if choice2=="PIE CHART":
        k=st.selectbox("CHOOSE COLUMN",("None","Gadget Type", "Gender","Language", "Sentiment"))
        if k=="Gadget Type":
                freq=(df['Gadget Type'].value_counts().to_list())
                label=df['Gadget Type'].value_counts().index
                fig=px.pie(values=freq,names=label)
                st.plotly_chart(fig)
        elif k=="Gender":
                freq=(df['Gender'].value_counts().to_list())
                label=df['Gender'].value_counts().index
                fig=px.pie(values=freq,names=label)
                st.plotly_chart(fig)
        elif k=="Language":
                freq=(df['Language'].value_counts().to_list())
                label=df['Language'].value_counts().index
                fig=px.pie(values=freq,names=label,)
                st.plotly_chart(fig)
        elif k=="Sentiment":
                freq=(df['Sentiment'].value_counts().to_list())
                label=df['Sentiment'].value_counts().index
                fig=px.pie(values=freq,names=label,)
                st.plotly_chart(fig)
        else:
                pass

    elif choice2=="HISTOGRAM":
        k=st.selectbox("CHOOSE COLUMN",("None","Gadget Type", "Gender","Language"))
        if k!='None':
            fig=px.histogram(df,x=k,color=df['Sentiment'])
            st.plotly_chart(fig)

    elif choice2=="SCATTERPLOT":
        k=st.selectbox("CHOOSE NUMERIC VALUE COLUMN",("None", "Gadget Type","Gender","Language"))
        if k!="None":
                try:
                        fig=px.scatter(df,x=k,y="Sentiment")
                        st.plotly_chart(fig)
                except Exception as e:
                        st.write("Please try with a Numeric Column")
                        st.rerun()