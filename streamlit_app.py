import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd

st.title("Zena's Amazing Athleisure Catalog")

# Establish connection to Snowflake
try:
    cnx = st.connection('snowflake')
    session = cnx.session()
except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
    st.stop()

# Get a list of colors for a drop list selection
try:
    table_colors = session.sql("SELECT color_or_style FROM catalog_for_website")
    pd_colors = table_colors.to_pandas()
    st.write("Available colors/styles:", pd_colors['COLOR_OR_STYLE'].tolist())
except Exception as e:
    st.error(f"Error fetching color options: {e}")
    st.stop()

# Output the list of colors into a drop list selector 
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors['COLOR_OR_STYLE'].tolist())

# Build the image caption now
product_caption = f'Our warm, comfortable, {option} sweatsuit!'

# Use the color selected to get all the info from the database
try:
    # Format the SQL query with the selected option directly
    query = f"""
        SELECT file_name, price, size_list, upsell_product_desc, file_url 
        FROM catalog_for_website 
        WHERE color_or_style = '{option}'  -- Ensure the value is safely escaped if needed
    """
    table_prod_data = session.sql(query)
    pd_prod_data = table_prod_data.to_pandas()
except Exception as e:
    st.error(f"Error fetching product data: {e}")
    st.stop()

# Print available columns for debugging
st.write("Available columns in the product DataFrame:", pd_prod_data.columns.tolist())

# Check if the DataFrame is empty
if not pd_prod_data.empty:
    try:
        price = pd_prod_data['PRICE'].iloc[0]  # Ensure the column name is correct
        price = f'${price:.2f}'  # Format the price correctly
    except KeyError:
        st.error("Price data is not available.")
        st.stop()

    file_name = pd_prod_data.get('FILE_NAME', None)
    size_list = pd_prod_data.get('SIZE_LIST', None)
    upsell = pd_prod_data.get('UPSELL_PRODUCT_DESC', None)
    url = pd_prod_data.get('FILE_URL', None)

    # Check if the URL is valid before displaying
    if url:
        st.image(image=url, width=400, caption=product_caption)
    else:
        st.error("Image URL is not available.")
    
    # Display product details
    st.markdown(f'**Price:** {price}')
    st.markdown(f'**Sizes Available:** {size_list}')
    st.markdown(f'**Also Consider:** {upsell}')
else:
    st.error("No product data found for the selected color/style.")
