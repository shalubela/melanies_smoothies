# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose fruits of your choice for the customized smoothie!:apple::banana::mango::pineapple:
    """
)

cnx=st.connection("snowflake")
session=cnx.session()

customer_name=st.text_input('Name on Smoothie: ')
st.write("Here's the text input: ", customer_name)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
##st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    "Choose upto 5 ingredients"
    ,my_dataframe, max_selections=6
)
if ingredients_list :
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        ##st.write(my_insert_stmt)
        ##fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        #st.text(fruityvice_response.json())
        if fruityvice_response:
            st.write(":" + fruit_chosen.lower() + ": " + fruit_chosen + ' Nutrition Information:')
            fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('"""+ customer_name + """', '""" + ingredients_string + """')"""
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+customer_name+'!', icon="✅")
    

