import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
import dash_calendar

import plotly.express as px
import pandas as pd
from joblib import Parallel, delayed
import joblib
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components


def predict_flight_price(route, date,op):
    
    date1 = datetime.strptime('2024-01-01', "%Y-%m-%d")
    date2 = datetime.strptime(str(date), "%Y-%m-%d")

    date_difference = date2 - date1


    days_between = date_difference.days

    rr = []
    
    
    
    if(route[0]=="Banglore"):
        if(op==1):
            indigo_Ban_del = joblib.load('Indigo_Ban-del.pkl')
            res = indigo_Ban_del.predict(1095,1095+days_between+Days)
            rr = []
            for i in res:
                rr.append(int(i))
            
        else:
            jetair_Ban_del = joblib.load('JETAIR_Ben-del.pkl')
            res = jetair_Ban_del.predict(1095,1095+days_between+Days)
            rr = []
            for i in res:
                rr.append(int(i))
            
            

    elif(route[0]=="Kolkata"):
        if(op==1):
            airindia_kol_ban = joblib.load('AIRINDIA_Kol-Ban.pkl')
            res = airindia_kol_ban.predict(1095,1095+days_between+Days)
            rr = []
            for i in res:
                rr.append(int(i))
            
        else:
            jetair_kol_ban = joblib.load('JETAIR_Kol-Ban.pkl')
            res = jetair_kol_ban.predict(1095,1095+days_between+Days)
            rr = []
            for i in res:
                rr.append(int(i))
            

        
    elif(route[0]=="Delhi"):
        if(op==1):
            jetair_Del_koc = joblib.load('JETAIR_Del-koc.pkl')
            res = jetair_Del_koc.predict(1095,1095+days_between+Days)
            rr = []
            for i in res:
                rr.append(int(i))
            
        else:
            mul_Del_koc = joblib.load('Mul_Del-koc.pkl')
            res = mul_Del_koc.predict(1095,1095+days_between+Days)
            rr = []
            for i in res:
                rr.append(int(i))
            
    return rr[len(rr)-Days::]


    
    


def generate_monthly_predictions(selected_route, start_date):
   
    predictions = []
    predicted_price1 = predict_flight_price(selected_route, start_date,1)
    predicted_price2 = predict_flight_price(selected_route, start_date,2)
    current_date = start_date

    
    
    for i in range(0,len(predicted_price1)):
       
        
        predictions.append(
            {
                "title": predicted_price1[i],
                "color": "red",
                "start": current_date.strftime("%Y-%m-%d"),
                "end": current_date.strftime("%Y-%m-%d"),
                "resourceId": "a",
                "borderColor": "Gold",

      
            }
        )
        predictions.append(
            {
                "title": predicted_price2[i],
                "color": "BLUE",
                "start": current_date.strftime("%Y-%m-%d"),
                "end": current_date.strftime("%Y-%m-%d"),
                "resourceId": "a",
                "borderColor": "Gold",
                
            }
        )
        current_date += timedelta(days=1)
    
    return predictions

st.set_page_config(page_title="Flight Fare Analysis")

st.markdown(
    """
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Anta&display=swap" rel="stylesheet">
    </head>
    """,
    unsafe_allow_html=True
)

# Markdown with desired font style
st.markdown("<h1 style='font-family: Anta, sans-serif; color: #F7940B;'>Flight Fare Analysis: Unveiling Insights and Trends</h1>", unsafe_allow_html=True)



selected_date = st.date_input("Select Date", datetime.today())
From = {'Delhi','Kolkata','Banglore'}
sel_from = st.selectbox("From", list(From))
bang_delhi = ['Indigo','JetAirlines']
del_koc = ['JetAirlines','Multi-carriers']
kol_ban = ['AirIndia','JetAirlines']
if(sel_from=='Delhi'):
    l = ["Kochi"]
    sel_to = st.selectbox("To", l)


    st.markdown("<p style='color: red; font-family: Anta, sans-serif;'>{0}</p>".format(del_koc[0]), unsafe_allow_html=True)
    st.markdown("<p style='color: blue; font-family: Anta, sans-serif;'>{0}</p>".format(del_koc[1]), unsafe_allow_html=True)

    op1 = del_koc[0]
    op2 = del_koc[1]
elif(sel_from=='Kolkata'):
    l = ["Banglore"]
    sel_to = st.selectbox("To", l)
    st.markdown("<p style='color: red; font-family: Anta, sans-serif;'>{0}</p>".format(kol_ban[0]), unsafe_allow_html=True)
    st.markdown("<p style='color: blue; font-family: Anta, sans-serif;'>{0}</p>".format(kol_ban[1]), unsafe_allow_html=True)
    op1 = kol_ban[0]
    op2 = kol_ban[1]
if(sel_from=='Banglore'):
    l = ["Delhi"]
    sel_to = st.selectbox("To", l)

    st.markdown("<p style='color: red; font-family: Anta, sans-serif;'>{0}</p>".format(bang_delhi[0]), unsafe_allow_html=True)
    st.markdown("<p style='color: blue; font-family: Anta, sans-serif;'>{0}</p>".format(bang_delhi[1]), unsafe_allow_html=True)
    
    op1 = bang_delhi[0]
    op2 = bang_delhi[1]

selected_route = [sel_from,sel_to]
Days = st.number_input("Select Days - Analysis", min_value=7, max_value=40, value=7)

submit_checkbox = st.checkbox("Submit")



if submit_checkbox:
    
    events = generate_monthly_predictions(selected_route, selected_date)

    
    calendar_resources = [
        {"id": "a", "building": "Building A", "title": "Room A"},
        {"id": "b", "building": "Building A", "title": "Room B"},
        {"id": "c", "building": "Building B", "title": "Room C"},
        {"id": "d", "building": "Building B", "title": "Room D"},
        {"id": "e", "building": "Building C", "title": "Room E"},
        {"id": "f", "building": "Building C", "title": "Room F"},
    ]

    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "resources": calendar_resources,
        "selectable": "true",
    }

   
    state = calendar(
        events=events,
        options=calendar_options,
        custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;

        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 3rem;
        }
        """,
        key="daygrid",  
        
        
    )

  

    
    if state.get("eventsSet") is not None:
        st.session_state["events"] = state["eventsSet"]

    
    
    operators = [op2, op1]
    prices = []
    opp2 = []
    opp1 = []
    dates = []
    for i in range(0,len(events),1):
        if(i%2==0):
            opp2.append(events[i]['title'])
            dates.append(events[i]['start'])
    prices.append(opp2)
    for i in range(1,len(events),1):
        if(i%2==1):
            opp1.append(events[i]['title'])
    prices.append(opp1)
    line_colors = ['BLUE','red']
   

    
   
    
   
    plot_type = st.selectbox('Select plot type', ['Line Plot', 'Scatter Plot'])
    if plot_type == 'Line Plot':
        fig = go.Figure()

        for i, operator in enumerate(operators):
            fig.add_trace(go.Scatter(x=dates, y=prices[i], mode='lines', name=operator,line=dict(color=line_colors[i])))

        fig.update_layout(title='Analysis : Flight Fare',
                    xaxis_title='Date',
                    yaxis_title='Price (INR)',
                    template='plotly_white')

    
        st.plotly_chart(fig)
    elif plot_type == 'Scatter Plot':

        fig = px.scatter(title='Analysis : Flight Fare', labels={'x': 'Date', 'y': 'Price (INR)'})
        fig.add_scatter(x=dates, y=prices[1], mode='markers', name=operators[0], marker_color='blue')
        fig.add_scatter(x=dates, y=prices[0], mode='markers', name=operators[1], marker_color='red')

        st.plotly_chart(fig)

        
        # fig = px.scatter(title='Analysis : Flight Fare', labels={'x': 'Date', 'y': 'Price (INR)'})
        # fig.add_scatter(x=dates, y=prices[1],mode='markers', name=operators[0])
        # fig.add_scatter(x=dates, y=prices[0],mode='markers', name=operators[1])
        
        # st.plotly_chart(fig)



    
    

    
    


# .venv\Scripts\Activate.ps1