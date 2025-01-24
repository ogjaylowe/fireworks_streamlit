import streamlit as st

st.title("Page 1")

expected_passport_2_output = {"LN":"BENJAMIN","FN":"FRANKLIN","NATIONALITY":"USA","POB":"PROVINCE OF MASSACHUSETTS BAY, USA","DOB":"17 Jan 1706","EXP":"15 Jan 2028"}
st.write(f"expected output: {expected_passport_2_output}")