# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    "Choose fruits for your custom smoothie."
)
# option = st.selectbox('How would you like to be contacted?', ('Email','Cell Phone','Home Phone'))
# st.write('You wish to be cotacted by:', option)

# option = st.selectbox('What is your favourite fruit?',('Banana','Strawberries','Peaches'))
# st.write('Your favourite fruit is:',option)


session = get_active_session()

name_on_order = st.text_input("Name on Smoothie:", "Name")
st.write("The name on the Smoothie will be ", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# st.dataframe(data=my_dataframe,use_container_width=True)

ingredient_list =  st.multiselect(
    "Choose up to 5 ingredients:"
    ,my_dataframe
    ,max_selections = 5
)
if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)

    ingredients_string =''

    for fruit_chosen in ingredient_list: 
        ingredients_string += fruit_chosen +' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
