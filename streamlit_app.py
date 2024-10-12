import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

st.title("🧥 Zena's Amazing Athleisure Catalog 🧥")

# Establish connection to Snowflake
try:
    cnx = st.connection('snowflake')
    session = cnx.session()
except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
    st.stop()

# Get all product data from the database
try:
    table_prod_data = session.sql(
        """
        SELECT color_or_style, file_name, price, size_list, upsell_product_desc, file_url 
        FROM catalog_for_website;
        """
    )
    pd_prod_data = table_prod_data.to_pandas()
except Exception as e:
    st.error(f"Error fetching product data: {e}")
    st.stop()

# Check if the DataFrame is empty
if pd_prod_data.empty:
    st.error("No product data found.")
    st.stop()

# Display each product in a tile layout
num_columns = 5  # Number of tiles per row
num_products = len(pd_prod_data)

# Function to display a single product in a tile
def display_product_tile(product):
    try:
        file_url = product['FILE_URL']
        color_or_style = product['COLOR_OR_STYLE']
        price = '$' + str(product['PRICE']) + '0'
        size_list = product['SIZE_LIST']
        upsell = product['UPSELL_PRODUCT_DESC']

        # Display product image and information
        st.image(file_url, width=200, caption=color_or_style)
        st.markdown(f"**Price:** {price}")
        st.markdown(f"**Sizes Available:** {size_list}")
        st.markdown(f"**Also Consider:** {upsell}")
        
        # Redeem button
        if st.button(f"Redeem {color_or_style}"):
            st.success(f"Congrats! You've redeemed the {color_or_style} sweatsuit!")
    except KeyError:
        st.error("Product data is incomplete.")

# Create a grid of product tiles
for i in range(0, num_products, num_columns):
    cols = st.columns(num_columns)  # Create columns
    for j, col in enumerate(cols):
        if i + j < num_products:  # Ensure we don't exceed the number of products
            with col:
                display_product_tile(pd_prod_data.iloc[i + j])
