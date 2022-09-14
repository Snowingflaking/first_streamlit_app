import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))   #  without prefill
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])   # next step old line 18
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)   


# new section to display fruityvice api response - line 24 in lessons
# variables ---  after all below are done!
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# streamlit.text(fruityvice_response)

streamlit.header("Fruityvice Fruit Advice!")
# streamlit.text(fruityvice_response.json())  ----  commented out for next steps!


# take the json version and normalize it
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

# line 37 in exercise 12  - more inserts to the line for cleanup
# don't run anything past here till we trouble shoot   - new 9/14  moves all the imports to the top!
streamlit.stop()

# import snowflake.connector

# line 39 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#  old  my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
# old my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
# old streamlit.text("Hello from Snowflake:")
# old 2  streamlit.text("The fruit load list contains:")
# old streamlit.text(my_data_row)
streamlit.header("The fruit load list contains:")
# old 2  streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

# line 46
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)


# line 50 and 51
# this will not work correctly, but just go with it now
my_cur.execute ("insert into fruit_load_list values ('from streamlit')")
