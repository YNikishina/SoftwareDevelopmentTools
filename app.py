# importing libraries
import pandas as pd
import streamlit as st
import plotly.express as px
    
# loading dataset
df = pd.read_csv("./processed_vehicles_us.csv")
       
# creating header with checkbox
st.header('Market of used cars. Processed data')

st.write("""
##### Filter the data below:
""")

# if checkbox marked, only listings that are 10 days old or less will be shown
new_listings = st.checkbox('Include only young listings (only 10 days old or less)')
if new_listings is True:
     df = df[df.days_listed <= 10]
        
# creating filtered data by model and year
# creating a list of unique car models
model_choice = df['model'].unique()

# creating slider
made_choice = st.selectbox('Select model:', model_choice)

# year range for slider
min_year = 1900
max_year = int(df['year'].max())
year_range = st.slider(
     "Choose year",
     value = (min_year,max_year), min_value=min_year, max_value=max_year )

# creating list of years
actual_range=list(range(year_range[0], year_range[1]+1))

# filtering data with picked parameters and showing 5 first rows of filtered table 
filtered_df=df[(df.model==made_choice)&(df.year.isin(list(actual_range)))]
st.table(filtered_df.head(5))

# creating header
st.header('Price analysis')

st.write("""
###### Price by transmission, cylinders, body type, 4 wheel drive or not, condition, and color
""")

# histogram of price depending on transmission, cylinders, body type, is 4 wheel drive, condition, color
# creating list of parameters
list_of_param=['transmission','cylinders','type','is_4wd', 'condition', 'paint_color']
# creatins selectbox to choose the parameter for histogram
choice_of_param = st.selectbox('Split for price distribution', list_of_param)
# creating histogram 
fig1 = px.histogram(filtered_df, x="price", color=choice_of_param)
# setting title and axis labels
fig1.update_layout(title="<b> Split of price by {}</b>".format(choice_of_param), xaxis_title='Price', yaxis_title='Number of       listings')
# setting the range of the x-axis to be between 0 and 50000 to make visualization more clear
fig1.update_xaxes(range=[0, 50_000])
# displaing the histogram
st.plotly_chart(fig1)

st.write("""
###### Price by mileage and days listed
""")

# scatter plot of price depending on odometer and days_listed

# changing data type in "odometer" to integer
filtered_df['odometer'] = filtered_df['odometer'].astype(float).astype(int)
# creating list of parameters
list_of_param_2=['odometer','days_listed']
# creating selectbox to choose the parameter for scatter plot
choice_of_param_2 = st.selectbox('Price dependency on ', list_of_param_2)
#creating scatter plot
fig2 = px.scatter(filtered_df, x="price", y=choice_of_param_2, color="condition", hover_data=['year'])
# setting title
fig2.update_layout(title="<b> Price vs {}</b>".format(choice_of_param_2))
# setting the range of the x-axis and y-axis 
fig2.update_xaxes(range=[0, 50_000])
# displaing the plot
st.plotly_chart(fig2)






#streamlit run app.py 
