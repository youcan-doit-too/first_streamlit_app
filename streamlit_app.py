import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New healthy Diner!")

streamlit.header("Breakfast Menu!")

streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale & Spinach Smoothie")
streamlit.text("🐔 Boiled Egg")
streamlit.text("🥑🍞 Avocado Toast")


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#read csv file
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Set index as Fruit name column
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include - default in square brackets
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

#Display only selected fruits on the page.
streamlit.dataframe(fruits_to_show)

#New section for FruityVice
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.write('The user entered ', fruit_choice)
  
  if not fruit_choice:
       streamlit.error("Please select a fruit to get information.")
  else:
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
       #streamlit.text(fruityvice_response.json())
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       #streamlit.dataframe(fruityvice_normalized.set_index('name'))
       streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#Let user add a fruit:
new_fruit = streamlit.text_input("What fruit would you like to add?")
streamlit.write('Thanks for adding', new_fruit)

my_cur.execute("INSERT INTO FRUIT_LOAD_LIST values ('from streamlit') ")
