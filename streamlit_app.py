# # Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
# Write directly to the app
st.title("🥤 Customise Your Smoothie!🥤")
st.title("My Parents New Healthier Diner")
st.write("""
Choose the fruits you want in your custom smoothie!
""")

Name_on_order = st.text_input('Name_on_Smoothie:')
st.write('The name on youe smoothies will be:', Name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect (
    'choose up to 5 ingredients:'
     , my_dataframe,
    max_selections=5)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
  #  st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','"""+Name_on_order+"""')"""

    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert :
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")




# # Import Python packages
# import streamlit as st
# from snowflake.snowpark.functions import col

# st.title("🥤 Customise Your Smoothie!🥤")
# st.title("My Parents New Healthier Diner")
# st.write("Choose the fruits you want in your custom smoothie!")

# # Input for name on smoothie
# Name_on_order = st.text_input('Name_on_Smoothie:')
# st.write('The name on your smoothie will be:', Name_on_order)

# # Connect to Snowflake and create session
# cnx = st.connection("snowflake")
# session = cnx.session()

# # Load fruit options from Snowflake table
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# # Show multi-select box for fruits, max 5
# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     my_dataframe.collect(),  # collect() to get local list of Rows
#     max_selections=5
# )

# if ingredients_list:
#     # Extract fruit names from Row objects
#     fruit_names = [row['FRUIT_NAME'] for row in ingredients_list]

#     # Join fruit names into single string
#     ingredients_string = ' '.join(fruit_names)

#     # Parameterized insert statement with bind variables (placeholders)
#     my_insert_stmt = "INSERT INTO smoothies.public.orders (ingredients, Name_on_order) VALUES (?, ?)"

#     st.write("SQL Statement (parameterized):", my_insert_stmt)
#     st.write("Ingredients:", ingredients_string)
#     st.write("Name on order:", Name_on_order)

#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         try:
#             # Bind parameters safely
#             session.sql(my_insert_stmt).bind((ingredients_string, Name_on_order)).collect()
#             st.success('Your Smoothie is ordered!', icon="✅")
#         except Exception as e:
#             st.error("Failed to insert order. Check your input and try again.")
#             st.exception(e)




