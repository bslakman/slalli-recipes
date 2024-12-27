import pandas as pd
import streamlit as st

def ingredient_list_for_recipe(recipe_name: str) -> pd.DataFrame:
    grocery_list = {}
    ingredients = list(df[df["Recipe Name"] == recipe_name]["Ingredient"])
    for item in ingredients:
        name_and_quantity = item.split(", ")
        if len(name_and_quantity) == 1:
            grocery_list[name_and_quantity[0]] = {"quantity": 1, "unit": None}
        elif len(name_and_quantity) >= 2:
            name = name_and_quantity[0]
            quantity_and_unit = name_and_quantity[-1].split()
            if len(quantity_and_unit) == 2:
                grocery_list[name] = {"quantity": quantity_and_unit[0], "unit": quantity_and_unit[1]}
            else:
                grocery_list[name] = {"quantity": quantity_and_unit[0], "unit": None}
            if len(name_and_quantity) > 2:
                grocery_list[name]["descriptor"] = name_and_quantity[1]
        else:
            print("Invalid ingredient: " + item)
    return pd.DataFrame(grocery_list).transpose().reset_index(names="ingredient").sort_values(["unit", "ingredient"])


url = f"https://docs.google.com/spreadsheets/d/{st.secrets['GOOGLE_SPREADSHEET_ID']}/export?format=csv&gid={st.secrets['GOOGLE_SHEET_GID']}"
df = pd.read_csv(url)
df.dropna(subset=["Recipe Name"], inplace=True)
links = df.dropna(subset=["Link to Recipe"])[["Recipe Name", "Link to Recipe"]]
links.rename(columns={"Link to Recipe": "Source"}, inplace=True)
links["Link to Recipe"] = links["Source"].apply(lambda source: source if "http" in source else "")
links = links[["Recipe Name", "Link to Recipe", "Source"]]

st.title("Slalli Recipes")
selected_recipe = st.dataframe(links, hide_index=True,
             column_config={"Link to Recipe":
                                st.column_config.LinkColumn(display_text="Click for recipe")},
             height=500,
             on_select="rerun",
             )
print(selected_recipe)
if len(selected_recipe["selection"]["rows"]) > 0:
    recipe_name = links.iloc[selected_recipe["selection"]["rows"][0]]["Recipe Name"]
    print(recipe_name)
    selected_recipe_df = ingredient_list_for_recipe(recipe_name)
    st.subheader(recipe_name)
    st.dataframe(selected_recipe_df, hide_index=True, height=500, width=500)
