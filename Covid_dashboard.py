#IMPORT LIBRARIES
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import plotly.express as px


#WEB PAGE CONFIGURATION
st.set_page_config(page_title ="My Webpage")  # you can add the argument layout = "wide"


#INTRODUCE PROJECT COLLABORATORS
from PIL import Image
with st.expander("Click to view project members and the goal of this project"):
    col1, col2, col3 = st.columns(3)
    with col1:
        #st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">'great'</p>', unsafe_allow_html=True)
        st.write("Senior Engineer (Nazanin)")
        image = Image.open(r'C:\Users\Nana\nazanin.jpg')
        st.image(image, use_column_width=True)

    with col2:
        st.write("Technical Lead (Ernest)")
        image = Image.open(r'C:\Users\Nana\ernest.jpg')
        st.image(image,use_column_width=True )


    with col3:
        st.write("Team Engineer (Rima)")
        image = Image.open(r'C:\Users\Nana\Reema.jpg')
        st.image(image, use_column_width=True)


    st.write("""
        This project is an initiative of the Data-Cirle of the Redi School of Digital Integration.
        The project deploys a fully interactive web analytics app using the
        streamlit library and other python dependencies.
        The goal is to improve the competence of the team members in designing
        fully functional interactive web base applications
     """)





#USE REQUESTS TO PULL ANIMATION FROM LOTTIE WEBSITE
@st.cache
def load_lottieurl(url):
    r =requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_1KyL2Q.json")
st_lottie(lottie, height =100, key ="covid")


#INSERT COVID PICTURES
from PIL import Image
with st.container():
    # Create headers
    st.markdown("<h1 style='text-align: center; color: green;'>COVID-19 Live Interactive Dashboard</h1>", unsafe_allow_html=True)
    left_col, right_col = st.columns(2)
    with left_col:
         image = Image.open(r'C:\Users\Nana\analytics.jpg')  # Put r in front of the file directory to be able to call the picture.
         st.image(image, width = 320)
    with right_col:
         image = Image.open(r'C:\Users\Nana\update.jpg')
         st.image(image, width = 300)
st.write("This analytics app provides real time updates on Covid-19 incidence around the world with Streamlit")

#DATA EXTRACTION 
with st.container():
    st.write("---")
    df = pd.read_csv("https://raw.githubusercontent.com/Brilla1234/COVID-19-WEB-ANALYTICS-APP/main/covid%20(5).csv") 
    #df.dropna(axis =0, how='any', thresh=None, subset=None, inplace=True)
    
# Create an interaction
check = st.checkbox("Check to display raw data")
if check:
    data_load_state = st.text('Loading data...')
    st.dataframe(df)
    data_load_state.text('Loading data...done!')


@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')
csv = convert_df(df)
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='Covid.csv',
     mime='text/csv',
 )
# CREATE RELEVANT GROUPBY'S FOR THE DATA  ANALYSIS
t_death = df.groupby(["continent","iso_code",'quarter','location'])["total_deaths"].mean().sort_values(ascending = False).reset_index()#Total deaths
t_case = df.groupby(["continent","iso_code",'quarter','location'])["total_cases"].mean().sort_values(ascending = False).reset_index()#Total cases
t_test = df.groupby(["continent","iso_code",'quarter','location'])["total_tests"].mean().sort_values(ascending = False).reset_index()# total_tests
t_vac = df.groupby(["continent","iso_code",'quarter','location'])["total_vaccinations"].mean().sort_values(ascending = False).reset_index() 
t_case1 = t_case[t_case['total_cases'].notna()]  # select observations which are not missing into a new dataframe

#CREATE WIDGETS FOR THE APP
# Drop down list for our countries
st.sidebar.header("Visualisation settings")    
country_box = st.sidebar.selectbox(
    "Select a country",
    ("Germany", "Ghana", "USA")
)
# Visualization Selector 
visual_box = st.sidebar.selectbox(
    "What type of visualization do you want to view?",
    ("Spatial visualizations", "Barplots", "Line Charts", "Radar Charts")
)

if country_box == "Germany" and visual_box == "Line Charts":
     fig = px.line(ger, x="quarter", y="total_tests", title = "Test Trend for Germany")  #  Line chart
     st.plotly_chart(fig, use_column_width=True)

elif country_box == "USA" and visual_box == "Radar Charts":
    st.write("Radar Chart for the United States")
    dff = pd.DataFrame(dict(
    r=[79000000, 14000000,  50000000, 33000000 ],
    theta=['Total deaths','ICU patients','Total vaccinations',
           'Total hospitalizations']))
    fig = px.line_polar(dff, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_column_width=True)



#VISUALIZATIONS  (Barplots)
with st.container():
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("<h1 style='text-align: right; color: blue;'>Barplots</h1>", unsafe_allow_html=True)        
    with right_col:
        lottie = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_2p5ywtpt.json")
        st_lottie(lottie, height =150, key ="bar")

with st.expander("ClICK TO VIEW TOTAL DEATHS BY CONTINENT & COUNTRY"):
    with st.container():
             fig = px.bar(t_death, y='total_deaths', x='continent', color ='iso_code', title="Total deaths by Continent & Country")
             st.plotly_chart(fig)

with st.expander("ClICK TO VIEW TOTAL CASES BY CONTINENT & COUNTRY"):
    with st.container():
         fig = px.bar(t_case, y='total_cases', x='continent', color ='iso_code', title="Total cases by Continent & Country")
         st.plotly_chart(fig)



with st.expander("ClICK TO VIEW TOTAL TESTS BY CONTINENT & COUNTRY"):           
    with st.container():
            fig = px.bar(t_test, x="continent", y="total_tests", color="iso_code", title="Total Tests by Country & Continent")
            st.plotly_chart(fig)

with st.expander("ClICK TO VIEW TOTAL VACCINATIONS BY CONTINENT & COUNTRY"):           
    with st.container():
             fig = px.bar(t_vac, x="continent", y="total_vaccinations", color="iso_code", title="Total Vaccinations by Country & Continent")
             st.plotly_chart(fig)


#VISUALIZATIONS  (Geospatial)
with st.container():
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("<h1 style='text-align: right; color: blue;'>Geo-Analysis</h1>", unsafe_allow_html=True)        
    with right_col:
        lottie = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_B6txqj.json")
        st_lottie(lottie, height =100, key ="globe")

st.write("---")        
map = st.radio(
     "CLICK TO CHANGE TO A DIFFERENT MAP",
     ('Map of Total deaths', 'Map of Total Cases', 'Map of Total Tests', 'Map of Total Vaccinations'))

if map == 'Map of Total deaths':
     st.write('Rendering image...')
     fig = px.choropleth(t_death, locations='iso_code',
                        projection="cylindrical stereographic",
                  color='total_deaths', scope ="world", title ="Total Deaths Across the Globe")
     st.plotly_chart(fig, use_column_width=True)  # Use different map types for the geospatial and put them in columns

elif map == 'Map of Total Vaccinations':
    st.write('Rendering image...')
    fig = px.choropleth(t_vac, locations='iso_code',
                        projection="cylindrical stereographic",
                  color='total_vaccinations', scope ="world", title ="Total Vaccinations Across the Globe")
    st.plotly_chart(fig, use_column_width=True)  # Use different map types for the geospatial and put them in columns


elif map == 'Map of Total Cases':
     st.write('Rendering image...')
     fig = fig = px.scatter_geo(t_case1, locations="iso_code", color="continent",
                     hover_name="location", size="total_cases",
                     projection="natural earth")
     st.plotly_chart(fig, use_column_width=True)  # Use different map types for the geospatial and put them in columns

elif map == 'Map of Total Tests':    
     st.write('Rendering image...')
     fig = px.choropleth(t_test, locations='iso_code',
                        projection="natural earth",
                  color='total_tests', scope ="world", title ="Total Tests Across the Globe")
     st.plotly_chart(fig, use_column_width=True)  # Use different map types for the geospatial and put them in columns

#LINE GRAPHS  ()
st.write("---") 
with st.container():
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("<h1 style='text-align: right; color: blue;'>TRENDS</h1>", unsafe_allow_html=True)        
    with right_col:
        lottie = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_iqfq0ogz.json")
        st_lottie(lottie, height =100, key ="trends")

with st.container():
    fig = px.line(df, x="date", y="total_deaths", color='location', title = "Death Trend")
    st.plotly_chart(fig, use_column_width=False)

with st.container():
    fig = px.line(df, x="date", y="total_vaccinations", color='location', title = "Vaccination Trend")
             #fig.update_layout(paper_bgcolor="black")
    st.plotly_chart(fig, use_column_width=True)

with st.container():
     fig = px.line(df, x="date", y="total_cases", color='location', title = "Cases Trend")
     st.plotly_chart(fig, use_column_width=False)

with st.container():
     fig = px.line(df, x="date", y="total_tests", color='location', title = "Test Trend")
     st.plotly_chart(fig, use_column_width=False)
