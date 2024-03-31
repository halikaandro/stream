import os

import streamlit as st
from pages import footer, image_upscaler, upscale_model_weights

# Initialize page config
st.set_page_config(
    page_title="FreeStream: Upscale Images with Real-ESRGAN", page_icon="🖼️"
)
st.title("🖼️Real-ESRGAN")
st.header(":green[_Upscale your images_]", divider="red")
st.caption(":violet[_This image upscaler is free for life._]")

# Show footer
st.markdown(footer, unsafe_allow_html=True)

# Create the sidebar
st.sidebar.subheader("__User Panel__")
st.sidebar.markdown(
    """
    Notice:
    
    Larger images will experience drastically longer processing times on higher upscaling factors, and may crash the application. For example, an image of 1301x851 with a 4x upscale factor took 507.988213 seconds.
    """
)
st.sidebar.divider()
# Add a file-upload button
uploaded_files = st.sidebar.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"],
    help="Upload a *SINGLE* image. Uploading a new image will interrupt the upscaling process.",
    key="image_to_upscale",
)

# Get the list of upscale factors from the dictionary
upscale_factors = list(upscale_model_weights.keys())
# Create a radio button widget with the list of upscale factors
scale_radio = st.sidebar.radio(
    label="Select an upscaling factor:",
    options=upscale_factors,  # Use the list of upscale factors
    index=upscale_factors.index(2),  # Set the default index to 2
    key="upscale_factor",
    horizontal=True,  # Display the radio buttons horizontally
    help="Choose your scale factor. When changing the scale while there's an uploaded image, image upscaling will begin immediately.",
)

# Create two columns with a single row to organize the UI
left_image, right_image = st.columns(2)
# Define a container for image containers
image_showcase = st.container()  # holds other containers

with image_showcase:  # add a try/except block
    if uploaded_files:
        # Show the uploaded image
        with left_image:
            st.image(uploaded_files)  # Latest uploaded image

        # Upscale and show the upscaled image
        with right_image:
            st.image(
                image_upscaler(image=uploaded_files, scale=scale_radio)
            )  # Latest uploaded image
