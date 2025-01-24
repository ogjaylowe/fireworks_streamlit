import streamlit as st
import plotly.graph_objs as go
import numpy as np
from PIL import Image

def create_percentage_plot(subheader="", match_rate=0):
    # Gauge Chart for Exact Match Rate
    fig_match_rate = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = match_rate,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': subheader},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
            'steps' : [
                {'range': [0, 50], 'color': "lightcoral"},
                {'range': [50, 100], 'color': "lightgreen"}
            ]
        }
    ))
    fig_match_rate.update_layout(height=300)
    return fig_match_rate

st.title("Performance Metrics")
st.write("all evaluations performed using 100 iterations")
st.write("Exact match means all parameters perfectly match expected output.")
st.write("- Ex. Province of Massachusetts and Massachusetts would score negatively")
st.write("Average match means parameters have acceptable overlap.")
st.write("- Ex. Province of Massachusetts and Massachusetts would score positively")

st.subheader("Driver Licence 1")
performance_data_dl1 = {
    'exact_match_rate': 0.22, 
    'average_match_percentage': 87.0, 
}

col1, col2, col3 = st.columns(3)
with col1:
    image = Image.open("test_imagery/License 1.png")
    st.image(image, width=300)  # Set a fixed width of 300 pixels
with col2:
    st.plotly_chart(create_percentage_plot("Exact Match %", performance_data_dl1['exact_match_rate'] * 100))
with col3:
    st.plotly_chart(create_percentage_plot("Average Match %", performance_data_dl1['average_match_percentage']))


st.subheader("Driver Licence 2")
performance_data_dl2 = {
    'exact_match_rate': 0.31, 
    'average_match_percentage': 93.0, 
}

col1, col2, col3 = st.columns(3)
with col1:
    image = Image.open("test_imagery/License-2.jpg")
    st.image(image, width=300)  # Set a fixed width of 300 pixels
with col2:
    st.plotly_chart(create_percentage_plot("Exact Match %", performance_data_dl2['exact_match_rate'] * 100))
with col3:
    st.plotly_chart(create_percentage_plot("Average Match %", performance_data_dl2['average_match_percentage']))


st.subheader("Driver Licence 3 - after rotation")
performance_data_dl3 = {
    'exact_match_rate': 0.18, 
    'average_match_percentage': 78.0, 
}

col1, col2, col3 = st.columns(3)
with col1:
    image = Image.open("test_imagery/License-3.jpeg")
    st.image(image, width=300)  # Set a fixed width of 300 pixels
with col2:
    st.plotly_chart(create_percentage_plot("Exact Match %", performance_data_dl3['exact_match_rate'] * 100))
with col3:
    st.plotly_chart(create_percentage_plot("Average Match %", performance_data_dl3['average_match_percentage']))


st.subheader("Passport 1")
performance_data_p1 = {
    'exact_match_rate': 0.26, 
    'average_match_percentage': 96.0, 
}

col1, col2, col3 = st.columns(3)
with col1:
    image = Image.open("test_imagery/passport-1.jpeg")
    st.image(image, width=300)  # Set a fixed width of 300 pixels
with col2:
    st.plotly_chart(create_percentage_plot("Exact Match %", performance_data_p1['exact_match_rate'] * 100))
with col3:
    st.plotly_chart(create_percentage_plot("Average Match %", performance_data_p1['average_match_percentage']))

st.subheader("Passport 2 - after rotation")
performance_data_p1 = {
    'exact_match_rate': 0.21, 
    'average_match_percentage': 95.0, 
}

col1, col2, col3 = st.columns(3)
with col1:
    image = Image.open("test_imagery/passport-2.jpg")
    st.image(image, width=300)  # Set a fixed width of 300 pixels
with col2:
    st.plotly_chart(create_percentage_plot("Exact Match %", performance_data_p1['exact_match_rate'] * 100))
with col3:
    st.plotly_chart(create_percentage_plot("Average Match %", performance_data_p1['average_match_percentage']))