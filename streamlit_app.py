import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

st.title("Zena's Amazing Athleisure Catalog")

# Establish connection to Snowflake
# Connect to Snowflake
try:
    cnx = st.connection('snowflake')
    session = cnx.session()
except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
    st.stop()

# Get a list of colors for a drop list selection
table_colors = session.sql("SELECT color_or_style FROM catalog_for_website")
pd_colors = table_colors.to_pandas()

# Output the list of colors into a drop list selector 
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors['COLOR_OR_STYLE'].tolist())

# Build the image caption now
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the color selected to go back and get all the info from the database
table_prod_data = session.sql("""
    SELECT file_name, price, size_list, upsell_product_desc, file_url 
    FROM catalog_for_website 
    WHERE color_or_style = :color
""", color=option)

# Convert the result to a pandas DataFrame
pd_prod_data = table_prod_data.to_pandas()

# Print available columns for debugging
st.write("Available columns in the product DataFrame:", pd_prod_data.columns.tolist())

# Check if the DataFrame is empty
if not pd_prod_data.empty:
    try:
        price = pd_prod_data['PRICE'].iloc[0]  # Ensure the column name is correct
        price = '$' + str(price) + '0'
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
    st.markdown('**Price:** ' + price)
    st.markdown('**Sizes Available:** ' + str(size_list))
    st.markdown('**Also Consider:** ' + upsell)
else:
    st.error("No product data found for the selected color/style.")
