import pandas as pd
import streamlit as st
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy

# Set page configuration
st.set_page_config(page_title="NBA EDA", page_icon="🏀", layout="wide")

st.markdown("""
Exploratory Data Analysis (EDA) of NBA Player Stats
""")

st.markdown("<hr style='border:1px solid red'>", unsafe_allow_html=True)

st.sidebar.header('User Input Features')
st.sidebar.markdown("<hr style='border:1px solid red'>", unsafe_allow_html=True)

selected_year = st.sidebar.selectbox('Pick a Year', list(reversed(range(1950,2020))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    
    num_cols = raw.select_dtypes(include="number").columns
    raw[num_cols] = raw[num_cols].fillna(0)
    obj_cols = raw.select_dtypes(include=["object", "string"]).columns
    raw[obj_cols] = raw[obj_cols].fillna("")
    raw["Awards"] = raw["Awards"].replace(0, "")
    raw["Awards"] = raw["Awards"].astype(str)

    #raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    # remove players who played in multiple teams during the season
    playerstats = playerstats[
    ~playerstats['Team'].isin(['2TM', '3TM', 0])]
    playerstats['Team'] = playerstats['Team'].astype(str)
    return playerstats

playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats['Team'].unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
sorted_unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', sorted_unique_pos, sorted_unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'''
    <a href="data:file/csv;base64,{b64}"
    download="nba.csv"
    style="
        color: white;
        background-color: #1f77b4;
        padding: 10px 15px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;">
    📥 Download CSV File
    </a>
    '''
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap

st.markdown("<hr style='border:1px solid red'>", unsafe_allow_html=True)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_numeric = df_selected_team.select_dtypes(include='number')
    corr = df_numeric.corr()

    mask = numpy.zeros_like(corr)
    mask[numpy.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True, cmap="RdYlGn", ax=ax)
    st.pyplot(f)


st.markdown("<hr style='border:1px solid red'>", unsafe_allow_html=True)



