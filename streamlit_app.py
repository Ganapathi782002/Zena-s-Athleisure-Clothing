import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

st.title("🏆 Redeem Your Points Here 🏆")

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

# Custom CSS for better layout
st.markdown("""
    <style>
    .product-card {
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f0f0;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    .product-price {
        font-size: 18px;
        font-weight: bold;
        color: #ff5722;
        margin: 10px 0;
    }
    .redeem-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .redeem-btn:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Function to display a single product tile with additional details on click
def display_product_tile(product):
    try:
        file_url = product['FILE_URL']
        color_or_style = product['COLOR_OR_STYLE']
        price = '' + str(product['PRICE']) + '0'
        size_list = product['SIZE_LIST']
        upsell = product['UPSELL_PRODUCT_DESC']

        # Display product in a card-like format
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        # Display product image
        st.image(file_url, width=250, caption=color_or_style)

        # Display only the price and redeem button initially
        st.markdown(f'<div class="product-price">{price}</div>', unsafe_allow_html=True)

        # Redeem button
        if st.button(f"Redeem"):
            #st.success(f"Congrats! You've redeemed the {color_or_style} sweatsuit!")
            pass

        # Toggle to show more details upon clicking
        with st.expander(f"More about {color_or_style}"):
            st.markdown(f"**Sizes Available:** {size_list}")
            st.markdown(f"**Also Consider:** {upsell}")

        st.markdown('</div>', unsafe_allow_html=True)

    except KeyError:
        st.error("Product data is incomplete.")

# Create a grid of product tiles with two per row and enough spacing
num_columns = 2  # Two products per row
num_products = len(pd_prod_data)

# Generate rows and columns for product display
for i in range(0, num_products, num_columns):
    cols = st.columns(num_columns)
    for j, col in enumerate(cols):
        if i + j < num_products:
            with col:
                display_product_tile(pd_prod_data.iloc[i + j])
