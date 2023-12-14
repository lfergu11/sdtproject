# loading the libraries
import streamlit as st
import pandas as pd
import plotly_express as px
import altair as alt

# load the data
df = pd.read_csv('vehicles_us.csv')

#------------------------------------

# data preprocessing & data engineering
# changing missing values in column to "0"
df.is_4wd = df.is_4wd.fillna(0)
# change column to int data type
df.is_4wd = df.is_4wd.astype(int)
# drop rows with missing values in column
df.dropna(subset=['model_year'], inplace=True)
# change model_year column to int data type
df.model_year = df.model_year.astype(int)
# change cylinders column to float data type
df.cylinders = pd.to_numeric(df['cylinders'])
# change odometer column to int data type
df.odometer = pd.to_numeric(df['odometer'])
# change date_posted column to datetime data type
df.date_posted = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')

# create new manufacturer column through the first word of model column
df.insert(loc=2,column='manufacturer',value=(df.model.apply(lambda x:x.split()[0])))
# remove manufacturer name from model column
df.model = df.model.str.split(n=1).str[1]
# create age column from model_year column (2019 is the newest model year)
df['age'] = 2020 - df.model_year
#capitalize manufacturer & model columns
df.manufacturer = df.manufacturer.str.capitalize()
df.model = df.model.str.capitalize()

# function to determine age group by vehicle age
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'
# create new column
df['age_category'] = df.age.apply(age_category) 

#------------------------------------

# create streamlit app
# title for web app
st.title('Car Sales Advertisements')

# header for data table
st.header('Data viewer')
st.write("""
         ##### Filter the data to see the ads by manufacturer, vehicle type & year
         """)

# selectbox for manufacturer filter
manufacturer_list = df.manufacturer.unique()
manufacturer_select = st.selectbox('Select manufacturer:', manufacturer_list)

# selectbox for vehicle type filter
vehicle_type_list = df.type.unique()
vehicle_select = st.selectbox('Select vehicle type:', vehicle_type_list)

# slider for year selection
min_year, max_year = int(df.model_year.min()),int(df.model_year.max())
year_range = st.slider(
     "Select year range:",
     value = (min_year,max_year),min_value=min_year,max_value=max_year
     )

# filtering the dataframe
year_list = list(range(year_range[0],year_range[1]+1))
filtered_table = df[(df.manufacturer==manufacturer_select) &
                   (df.type==vehicle_select) &
                   (df.model_year.isin(list(year_list)))]

# display filtered table
st.dataframe(filtered_table)

#-----------------------------

# header for first histogram
st.header('Distribution of vehicle types by the manufacturer')
# distribution of vehicle types by the manufacturer
fig1 = px.histogram(df, x='manufacturer', color='type')
st.plotly_chart(fig1)

# header for second histogram
st.header('Distribution of vehicle condition by vehicle age')
# distribution of condition by age_category
fig2 = px.histogram(df, x='age_category',
                    color='condition',
                    category_orders=dict(age_category=['>20','10-20','5-10','<5']))
st.plotly_chart(fig2)

# header for third histogram with checkbox
st.header('Price distribution between different manufacturers')
new_cars = st.checkbox('Display only new cars')
price_df = df
if new_cars:
    price_df = price_df[price_df.condition=='new']
# selectboxes for manufacturers
manufacturer1 = st.selectbox('Select first manufacturer:', manufacturer_list)
manufacturer2 = st.selectbox('Select second manufacturer:', manufacturer_list)
# filtering the dataframe
manufacturers_data = price_df[(price_df.manufacturer==manufacturer1)|(price_df.manufacturer==manufacturer2)]
# price distribution between manufacturers
fig3 = px.histogram(manufacturers_data,
                    x='price',
                    nbins=30,
                    color='manufacturer',
                    barmode='overlay')
st.plotly_chart(fig3)

#---------------------------------

# header for first scatterplot
st.header('Price correlations')
st.write("""
         ##### Check how price is affected by odometer, vehicle age or days listed
         """)
# selectbox for second variable
scatter_list = ['odometer','age','days_listed']
scatter_select = st.selectbox('Price dependency on ', scatter_list)
# scatterplot of price depending on scatter_select
fig4 = px.scatter(df,x='price', y=scatter_select, color = 'condition',
                  hover_data=['model_year'])
st.plotly_chart(fig4)






