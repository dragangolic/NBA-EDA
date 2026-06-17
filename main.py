import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(page_title="NBA EDA", page_icon="🏀", layout="wide")

df = pd.read_csv("./Data/nba.csv")
print(df.head())