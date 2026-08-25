#Custom Smoothy Order Form app
# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
# Sis: from snowflake.snowpark.context import get_active_session
import requests  
import pandas

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

# st.write("Your favorite fruit is:", option)
NAME_ON_ORDER = ""
NAME_ON_ORDER = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", NAME_ON_ORDER)

from snowflake.snowpark.functions import col

#SniS:
cnx = st.connection("snowflake")
session = cnx.session()
# SiS: session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
# Convert the Snowpark Datagram to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
    , max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+NAME_ON_ORDER+ """')"""

    time_to_insert = st.button('Submit Order')
    
    # if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

        
