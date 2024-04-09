import streamlit as st
import pandas as pd

st.write("""
# My first app
Hello *world!*
""")


df = pd.read_csv("C:\\Users\YQ\Desktop\pythonProject\知识系统\my_test_data.csv")
st.line_chart(df)
