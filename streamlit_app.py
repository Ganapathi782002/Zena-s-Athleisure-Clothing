import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

# Set the page width to wide for a better tile display
st.set_page_config(layout="wide")

st.title("🧥 Zena's Amazing Athleisure Catalog 🧥")
st.markdown("---")

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

# Custom CSS for a more polished look
st.markdown("""
    <style>
    .product-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .product-title {
        font-size: 18px;
        font-weight: bold;
        color: #2e7d32;
        margin-bottom: 10px;
    }
    .product-image {
        margin-bottom: 15px;
    }
    .product-info {
        margin-bottom: 10px;
    }
    .redeem-btn {
        background-color: #ff7043;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
    }
    .redeem-btn:hover {
        background-color: #f4511e;
    }
    </style>
""", unsafe_allow_html=True)

# Function to display a single product in a styled tile
def display_product_tile(product):
    try:
        file_url = product['FILE_URL']
        color_or_style = product['COLOR_OR_STYLE']
        price = '$' + str(product['PRICE']) + '0'
        size_list = product['SIZE_LIST']
        upsell = product['UPSELL_PRODUCT_DESC']

        # Display product in a styled card layout
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        st.image(file_url, width=250, caption=color_or_style, class_="product-image")
        st.markdown(f'<div class="product-title">{color_or_style} Sweatsuit</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-info"><strong>Price:</strong> {price}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-info"><strong>Sizes Available:</strong> {size_list}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-info"><strong>Also Consider:</strong> {upsell}</div>', unsafe_allow_html=True)

        # Redeem button
        if st.button(f"Redeem {color_or_style}", key=color_or_style):
            st.success(f"Congrats! You've redeemed the {color_or_style} sweatsuit!")

        st.markdown('</div>', unsafe_allow_html=True)
    except KeyError:
        st.error("Product data is incomplete.")

# Create a grid of product tiles with better formatting
num_columns = 3  # Number of tiles per row
num_products = len(pd_prod_data)

for i in range(0, num_products, num_columns):
    cols = st.columns(num_columns)  # Create columns
    for j, col in enumerate(cols):
        if i + j < num_products:  # Ensure we don't exceed the number of products
            with col:
                display_product_tile(pd_prod_data.iloc[i + j])
