import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title("Custom_Smoothie_Order_Form :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie.")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie is:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
fruit_df = session.table("smoothies.public.fruit_options") \
                  .select(col("Fruit_Name")) \
                  .collect()

fruit_list = [row["FRUIT_NAME"] for row in fruit_df]

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Submit order
if ingredients_list and name_on_order:
    ingredients_string = ", ".join(ingredients_list)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        insert_stmt = """
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES (%s, %s)
        """
        session.sql(insert_stmt, params=[ingredients_string, name_on_order]).collect()
        smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon")

    if smoothiefroot_response.status_code == 200:
    st.dataframe(
        smoothiefroot_response.json(),
        use_container_width=True
    )
        st.success("Your Smoothie is ordered!", icon="✅")

# ---- External API example ----
st.header("Fruit Nutrition Info")


else:
    st.error("Failed to fetch fruit data")
