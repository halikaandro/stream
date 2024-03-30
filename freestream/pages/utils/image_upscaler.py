import streamlit as st
import torch
from PIL import Image
from RealESRGAN import RealESRGAN
from .utility_funcs import logger
import datetime

# Define a dictionary to store model weights for different scales
upscale_model_weights = {
    2: "weights/RealESRGAN_x2plus.pth",
    4: "weights/RealESRGAN_x4plus.pth",
    # 8: "weights/RealESRGAN_x8plus.pth"
}

# Define a function to upscale images using HuggingFace and Torch
def image_upscaler(image: str, scale: int) -> Image:
    """
    Upscales the input image using the specified model and returns the upscaled image.

    Parameters:
    image (str): The file path of the input image.

    Returns:
    Image: The upscaled image.
    """

    # Assign the image to a variable
    img = Image.open(image)

    # Initialize the upscaler
    upscaler = RealESRGAN(
        device="cpu",
        scale=scale
    )

    # Load the corresponding model weight
    if scale in upscale_model_weights:
        upscaler.load_weights(
            upscale_model_weights[scale],
            # Download the model weight if it doesn't exist
            download=True,
        )
    else:
        logger.error("Scale factor not in supported model weights.")
    
    try:
        # Convert the opened image to RGB
        img = img.convert("RGB")
        logger.info("Image converted to RGB.")
    except Exception as e:
        logger.error(f"Failed to convert image to RGB. Error: {e}")

    try:
        # Capture start time
        start_time = datetime.datetime.now()
        
        # Upscale the image
        logger.info(
            f"\nStarted upscaling {img} at {datetime.datetime.now().strftime('%H:%M:%S')}..."
        )
        with st.spinner(
            f"Began upscaling: {datetime.datetime.now().strftime('%H:%M:%S')}..."
        ):
            upscaled_img = upscaler.predict(img)
            logger.info(
                f"\nFinished upscaling {img} at {datetime.datetime.now().strftime('%H:%M:%S')}."
            )
            
        # Capture end time
        end_time = datetime.datetime.now()
        
        # Calculate the process duration
        process_duration = end_time - start_time
        
        st.toast(f"Success! Upscaling took {process_duration.total_seconds()} seconds.", icon="✅")
    
    except Exception as e:
        logger.error(f"Failed to upscale image. Error: {e}")
        st.error(f"Failed to upscale image! Please try again.")

    return upscaled_img