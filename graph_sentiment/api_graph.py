# Import packages
# from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

"""
Creates and returns jsonified graphs to be sent out by the API.
Utilizes data collected from sentiment database.
"""

def create_graph(db_data) :
     # Check if db_data is of the proper format.
    if not isinstance(db_data, list) or not all(isinstance(subtuple, tuple) and len(subtuple) == 3 for subtuple in db_data):
        raise ValueError("Invalid input format. Expecting a list of subtuples of length 3.")

    if len(db_data) < 1:
        raise ValueError("No data to graph.")
    
    if not all(isinstance(subtuple[1], int) and (subtuple[1] == 0 or subtuple[1] == 1) for subtuple in db_data):
        raise ValueError("Improper sentiment values. Expecting 0 or 1.")

    if not all((isinstance(subtuple[2], int) or isinstance(subtuple[2], float)) and 0 <= subtuple[2] <= 100 for subtuple in db_data):
        raise ValueError("Sentiment scores out of range. Expecting values between 0 and 100 inclusive.")     

    # Extract columns from the data
    data = list(zip(*db_data))

    time_data = data[0]
    sentiment = data[1]
    score = data[2]
    new_score = []

    # Update score depending on value of sentiment
    i = 0
    while i < len(time_data):
        if sentiment[i] is not None:
            if sentiment[i] < 1:
                new_score.append(score[i])
            else:
                new_score.append(score[i] * -1)
        i += 1

    df = pd.DataFrame({'Time': time_data, 'Score': new_score})

    # Divide graph into positive and negative sentiment score
    mask = df['Score'] > 0
    df['Positive'] = np.where(mask, df['Score'], 0)
    df['Negative'] = np.where(mask, 0, df['Score'])

    # Hide points on x axis that are 0
    positive_dot_opacity=np.ones(len(df['Positive']))
    negative_dot_opacity=np.ones(len(df['Negative']))

    i = 0
    while i < len(positive_dot_opacity):
        if df['Positive'][i] == 0:
            positive_dot_opacity[i] = 0
        if df['Negative'][i] == 0:
            negative_dot_opacity[i] = 0
        i += 1
    
    #Create the graph and add the traces for positive and negative score
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Positive'], fill='tozeroy', name="Positive Sentiment", marker_color='green', marker=dict(opacity=positive_dot_opacity)))
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Negative'], fill='tozeroy', name="Negative Sentiment", marker_color='red', marker=dict(opacity=negative_dot_opacity)))
    fig.update_layout(template="simple_white", autotypenumbers='convert types')        
    fig.update_layout(
        title="<b>Sentiment Analysis<b>",
        xaxis_title="Time",
        yaxis_title="Score",
        font=dict(
            size=18,
            color="Black"
        ),
        yaxis=dict(
        range=[-120, 120]
        )
    )
    # Return graph as html div element
    return fig.to_html(full_html=False)


