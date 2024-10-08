import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

st.title("Zena's Amazing Athleisure Catalog")

# Connect to Snowflake
try:
    cnx = st.connection('snowflake')
    session = cnx.session()
except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
    st.stop()

# Get a list of colors for drop list selection
try:
    table_colors = session.sql("select color_or_style from catalog_for_website")
    pd_colors = table_colors.to_pandas()
except Exception as e:
    st.error(f"Error fetching colors: {e}")
    st.stop()

# Output the list of colors into a drop list selector
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors['color_or_style'])

# Build the image caption
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Get all the info from the database
try:
    table_prod_data = session.sql("select file_name, price, size_list, upsell_product_desc, file_url from catalog_for_website where color_or_style = :color", color=option)
    pd_prod_data = table_prod_data.to_pandas()
except Exception as e:
    st.error(f"Error fetching product data: {e}")
    st.stop()

# Assign each column of the row returned to its own variable
if not pd_prod_data.empty:
    price = '$' + str(pd_prod_data['price'].iloc[0]) + '0'  # Ensure the column name is correct
    file_name = pd_prod_data['file_name'].iloc[0]  # Ensure column names are correct
    size_list = pd_prod_data['size_list'].iloc[0]
    upsell = pd_prod_data['upsell_product_desc'].iloc[0]
    url = pd_prod_data['file_url'].iloc[0]

    # Display the info on the page
    try:
        st.image(image=url, width=400, caption=product_caption)
    except Exception as e:
        st.error("Error displaying the image.")
        st.write(e)

    st.markdown('**Price:** ' + price)
    st.markdown('**Sizes Available:** ' + size_list)
    st.markdown('**Also Consider:** ' + upsell)
else:
    st.error("No product data found for the selected color/style.")
