# # Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop

#converting snowpark dataframe to pandas dataframe
pf_df=my_dataframe.to_pandas()
st.dataframe(pf_df)
#st.stop

ingredients_list=st.multiselect (
    'choose up to 5 ingredients:'
     , my_dataframe,
    max_selections=5)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pf_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        

        
  #  st.write(ingredients_string)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','"""+Name_on_order+"""')"""

    st.write(my_insert_stmt)

    #st.stop()
    
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert :
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")







#####new code

# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests

# # Title and Intro
# st.title("🥤 Customise Your Smoothie!🥤")
# st.title("My Parents' New Healthier Diner")
# st.write("Choose the fruits you want in your custom smoothie!")

# # Input name
# Name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your smoothie will be:', Name_on_order)

# # Connect to Snowflake and retrieve data
# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# # Convert to pandas DataFrame
# pf_df = my_dataframe.to_pandas()
# st.dataframe(pf_df)

# # Fruit selection
# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     pf_df['FRUIT_NAME'].tolist(),
#     max_selections=5
# )

# # Display nutrition and search value
# if ingredients_list:
#     ingredients_string = ''
    
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#         search_on = pf_df.loc[pf_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         st.write(f'The search value for {fruit_chosen} is {search_on}.')

#         st.subheader(f'{fruit_chosen} Nutrition Information')
#         response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
#         if response.ok:
#             st.dataframe(response.json(), use_container_width=True)
#         else:
#             st.warning(f"Could not retrieve nutrition info for {fruit_chosen}")

#     # Insert order query
#     my_insert_stmt = f"""
#         insert into smoothies.public.orders(ingredients, Name_on_order)
#         values ('{ingredients_string.strip()}', '{Name_on_order}')
#     """
#     st.write(my_insert_stmt)

#     # Button to submit order
#     if st.button('Submit Order'):
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")










