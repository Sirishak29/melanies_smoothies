import pandas as pd

st.header("Fruit Nutrition Info")

if ingredients_list:
    nutrition_data = []

    for fruit in ingredients_list:
        api_url = f"https://my.smoothiefroot.com/api/fruit/watermelon"
        response = requests.get(api_url)

        if response.status_code == 200:
            fruit_json = response.json()

            nutrition_data.append({
                "Fruit": fruit_json["name"].title(),
                "Calories": fruit_json["nutritions"]["calories"],
                "Fat": fruit_json["nutritions"]["fat"],
                "Sugar": fruit_json["nutritions"]["sugar"],
                "Carbohydrates": fruit_json["nutritions"]["carbohydrates"],
                "Protein": fruit_json["nutritions"]["protein"]
            })
        else:
            st.warning(f"Nutrition data not available for watermelon")

    if nutrition_data:
        nutrition_df = pd.DataFrame(nutrition_data)
        st.dataframe(nutrition_df, use_container_width=True)
else:
    st.info("Select fruits to see nutrition information.")
