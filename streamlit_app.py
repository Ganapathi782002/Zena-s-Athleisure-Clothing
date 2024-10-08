import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

st.title("Zena's Amazing Athleisure Catalog")

# Establish connection to Snowflake
try:
    cnx = st.connection('snowflake')
    session = cnx.session()
except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
    st.stop()

# Get a list of colors for a drop-down selection
try:
    table_colors = session.sql("SELECT color_or_style FROM catalog_for_website")
    pd_colors = table_colors.to_pandas()
except Exception as e:
    st.error(f"Error fetching color options: {e}")
    st.stop()

# Output the list of colors into a drop list selector 
option = st.selectbox('Pick a Sweatsuit color or Style:', pd_colors['COLOR_OR_STYLE'].tolist())

# Build the image caption now
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the color selected to get all the info from the database
try:
    table_prod_data = session.sql(
        f"""
        SELECT file_name, price, size_list, upsell_product_desc, file_url 
        FROM catalog_for_website 
        WHERE color_or_style = '{option}';
        """
    )
    pd_prod_data = table_prod_data.to_pandas()
except Exception as e:
    st.error(f"Error fetching product data: {e}")
    st.stop()

# Check if the DataFrame is empty
if not pd_prod_data.empty:
    try:
        price = pd_prod_data['PRICE'].iloc[0]
        price = '$' + str(price) + '0'

        file_url = pd_prod_data['FILE_URL'].iloc[0]  # Fetch the pre-signed URL
        size_list = pd_prod_data['SIZE_LIST'].iloc[0]
        upsell = pd_prod_data['UPSELL_PRODUCT_DESC'].iloc[0]
    except KeyError:
        st.error("Product data is not available.")
        st.stop()
    
    # Display the image using the pre-signed URL
    if file_url:
        st.image(image=file_url, width=400, caption=product_caption)
    else:
        st.error("Image URL is not available.")
    
    # Display product details
    st.markdown('**Price:** ' + price)
    st.markdown('**Sizes Available:** ' + str(size_list))
    st.markdown('**Also Consider:** ' + upsell)
else:
    st.error("No product data found for the selected color/style.")
