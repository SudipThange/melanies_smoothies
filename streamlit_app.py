# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import os
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie:cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom smoothie.
  """
)

user_name = st.text_input("Name on Smoothie :cup_with_straw:")
st.write("The current entered name is: ", user_name)

# updated code
cnx = st.connection("snowflake")
session = cnx.session()
#--------------------------------

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"), col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width = True)
#st.stop()
                                                                                             
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients'
    ,my_dataframe
    ,max_selections = 5
)

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

if ingredients_list:
    ingredients_string = ''
    
    for fruits_chose in ingredients_list:
        ingredients_string += fruits_chose + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chose, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits_chose,' is ', search_on, '.')
      
        st.subheader(fruits_chose + 'Nutrition Information')
      
        smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/" + fruits_chose
        )
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    insert_stmt = """
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
    VALUES('"""+ ingredients_string +"""', '"""+ user_name +"""');
    """

    #st.write(insert_stmt)
    #st.stop()
    
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is Ordered ', icon = "✅")
