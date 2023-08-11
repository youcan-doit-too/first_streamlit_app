import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#All functions
def get_fruityvice_data(this_fruit_choice):
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       return fruityvice_normalized

def get_fruit_load_list():
       with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
            return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
       with my_cnx.cursor() as my_cur:
              my_cur.execute("INSERT INTO FRUIT_LOAD_LIST values ('" + :new_fruit "') ")
              return "Thanks for adding " + new_fruit

#main code
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
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

#Hit button to get fruit list
if streamlit.button('Get Fruit List'):
       my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
       my_data_rows = get_fruit_load_list()
       my_cnx.close()
       streamlit.dataframe(my_data_rows)

#Let user add a fruit:
input_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add new fruit to list'):
       my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
       back_from_function = insert_row_snowflake(input_fruit)
       my_cnx.close()
       streamlit.text(back_from_function)

