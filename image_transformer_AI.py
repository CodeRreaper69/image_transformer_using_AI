import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import io
import time
from dotenv import load_dotenv
import google.generativeai as genai
import os

#necessary env loading 
load_dotenv()

Google_API_KEY = os.getenv("API_KEY")

genai.configure(api_key=Google_API_KEY)



st.set_page_config(page_title="IMAGE_TRANSFORMATION USING AI", page_icon="⚛️")

st.title(":red[WELCOME TO IMAGE TRANSFORMATION USING GEN_AI]")
st.subheader(":rainbow[GET AI SUGGESTIONS AND GENERATIONS AT YOUR FINGER TIPS!]")

st.caption(":grey[TO ALL THOSE WHO SEEK ACTION, ACCORDING TO NEWTON, THERE ALWAYS LIES A REACTION]")
st.markdown("""
Created and Managed by [Sourabh Dey](https://linktr.ee/sourabhdey)
""")

def stream_words(string,t):
    for word in string:
        yield word
        time.sleep(t)

note_1 = ":green[For smartphone users, open this app in desktop mode for better experience]"

note_2 = """:orange[Click/Swipe on the sidebar or ">" this icon after the image has been added for the editing tools]"""

st.write_stream(stream_words(note_1,0.05))


note_3 = """:blue[Navigate to the AI CORNER after uploading the image for getting AI suggestions about the image and about editing the image, this is all about GenAI]"""

st.write_stream(stream_words(note_3,0.04))



# Function to load an image from uploaded file
def load_image(image_file):
    img = Image.open(image_file)
    return img

with st.expander(":violet[WHAT IS THIS ?]"):
    st.write(":green[FIRST UPLOAD THE IMAGE THEN THE MAGIC WILL HAPPEN!🤩]")
    st.write("""
        **GET TO THE AI CORNER FOR GETTING CUSTOM QUERIES AND REQUESTS ABOUT THE IMAGE BEING COMPLETED AND ALSO GET AI SUGGESTIONS ABOUT EDITING THE IMAGE**
        **How to Use IMAGE TRANSFORMER:**
        1. **Upload Image**: Click on the "Upload an image file to continue" button and select the image you want to edit. Supported formats include JPEG, PNG, BMP, and TIFF.

        2. **Editing Options**: Use the sidebar to apply various edits to your image:
            - **Resize**: Adjust the width and height of the image.
            - **Rotate**: Rotate the image by a specified angle or use the buttons to rotate left or right.
            - **Brightness**: Adjust the brightness of the image.
            - **Contrast**: Adjust the contrast of the image.
            - **Sharpness**: Adjust the sharpness of the image.
            - **Color**: Adjust the color saturation of the image.
            - **Pixel Value Adjustment**: Modify the pixel values with a specified factor.

        3. **Preview**: The main area displays both the original and edited images for comparison.

        4. **Save Edited Image**: Choose the format (JPEG, PNG, BMP, or TIFF) and download the edited image using the "Download Edited Image" button.

        5. **Convert Image Format**: Use the "Convert Image Format" option in the sidebar to convert the image to a different format and download it using the "Download Converted Image" button.

        6. **Done Editing**: Click the "DONE EDITING" button to finish the editing session and celebrate your work with some fun Streamlit effects.

        **Note**: Make sure to apply all desired changes before downloading the image to ensure all edits are included in the final download.

        Enjoy transforming your images with IMAGE_TRANSFORMER!
    """)






uploaded_file = st.file_uploader("Upload an image file to continue", type=["jpg", "jpeg", "png", "bmp", "tiff"], label_visibility = "visible" )

prompt = """Suggest some changes about the image for editing, tell on what scale I should keep the brightness,contrast,sharpness,color, from a scale of 1.00 to 2.00 each and
                about the pixel adjustment factor with which this image pixels can be multiplied with a number from a range of 1.00 to 10.00,
                so as to enhance the picture quality, just write some points about those values and also about the image, like 2-3 lines """

def image_prompter(photo,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt,image])
        output = response.text
        
    except ValueError:
        output = """What you asked might be unethical or in appropriate"""
    finally:
        return stream_words(output,0.001)


#st.toast(":orange[Click on the "<" after #the image has been added for the editing #tools]")

st.write_stream(stream_words(note_2,0.03))

if uploaded_file is not None:
    #st.toast(":rainbow[NOW START EDITING]")
    image = load_image(uploaded_file)
    

    # Sidebar for image editing options
    st.sidebar.header("Edit Image")
    
    # Resize
    st.sidebar.subheader("Resize")
    width = st.sidebar.number_input("Width", value=image.width, min_value=1)
    height = st.sidebar.number_input("Height", value=image.height, min_value=1)
    
    # Rotate
    st.sidebar.subheader("Rotate")
    angle = st.sidebar.slider("Angle", 0, 360, 0)
    left = st.sidebar.button("Rotate left")
    right = st.sidebar.button("Rotate right")
    
    # Adjust brightness
    st.sidebar.subheader("Brightness")
    brightness = st.sidebar.slider("Brightness", 0.0, 2.0, 1.0)
    
    # Adjust contrast
    st.sidebar.subheader("Contrast")
    contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0)
    
    # Adjust sharpness
    st.sidebar.subheader("Sharpness")
    sharpness = st.sidebar.slider("Sharpness", 0.0, 2.0, 1.0)
    
    # Adjust color
    st.sidebar.subheader("Color")
    color = st.sidebar.slider("Color", 0.0, 2.0, 1.0)
    
    # Adjust pixel values
    st.sidebar.subheader("Pixel Value Adjustment")
    pixel_value_factor = st.sidebar.slider("Pixel Value Factor", 1.0, 10.0, 1.0)
    
    # Apply edits to the image
    edited_image = image.copy()
    edited_image = edited_image.resize((width, height))
    edited_image = edited_image.rotate(angle)
    
    # Rotate on button press
    if right:
        edited_image = edited_image.rotate(90)
    elif left:
        edited_image = edited_image.rotate(270)
    
    # Adjust brightness
    brightness_enhancer = ImageEnhance.Brightness(edited_image)
    edited_image = brightness_enhancer.enhance(brightness)
    
    # Adjust contrast
    contrast_enhancer = ImageEnhance.Contrast(edited_image)
    edited_image = contrast_enhancer.enhance(contrast)
    
    # Adjust sharpness
    sharpness_enhancer = ImageEnhance.Sharpness(edited_image)
    edited_image = sharpness_enhancer.enhance(sharpness)
    
    # Adjust color
    color_enhancer = ImageEnhance.Color(edited_image)
    edited_image = color_enhancer.enhance(color)
    
    # Adjust pixel values
    edited_image = edited_image.point(lambda p: p * pixel_value_factor)
    
    # Layout to show both original and edited images
    col1, col2 = st.columns(2)
    with col1:
        st.header("Original Image")
        st.image(image, use_column_width=True)
    with col2:
        st.header("Edited Image")
        st.image(edited_image, use_column_width=True)
    
    # Save options
    st.sidebar.header("Save Image")
    save_option = st.sidebar.selectbox("Save edited image as", ["PNG","JPEG" , "BMP", "TIFF"])
    edited_image_io = io.BytesIO()
    if save_option == "JPEG" and edited_image.mode == "RGBA":
        edited_image = edited_image.convert("RGB")# Convert RGBA to RGB for JPEG
        edited_image.save(edited_image_io, format=save_option)
    if save_option == "JPEG":
        edited_image.save(edited_image_io, format="JPEG")
    elif save_option == "PNG":
        edited_image.save(edited_image_io, format="PNG")
    elif save_option == "BMP":
        edited_image.save(edited_image_io, format="BMP")
    elif save_option == "TIFF":
        edited_image.save(edited_image_io, format="TIFF")
    
    
    # File format converter
    st.sidebar.header("Convert Image Format")
    format_option = st.sidebar.selectbox("Convert to", ["JPEG", "PNG", "BMP", "TIFF"])
    converted_image_io = io.BytesIO()
    if format_option == "JPEG" and edited_image.mode == "RGBA":
        edited_image = edited_image.convert("RGB")  # Convert RGBA to RGB for JPEG
    
    edited_image.save(converted_image_io, format=format_option)

    
    
    
    #edited_image.save(converted_image_io, format=format_option)
    if st.download_button(
        label="Download Edited Image",
        data=edited_image_io.getvalue(),
        file_name=f"edited_image.{save_option.lower()}",
        mime=f"image/{save_option.lower()}"
    ):
        #st.snow()
        st.toast(":rainbow[THANKS FOR DOWNLOADING]")  
    if st.download_button(
        label="Download Converted Image",
        data=converted_image_io.getvalue(),
        file_name=f"converted_image.{format_option.lower()}",
        mime=f"image/{format_option.lower()}"
    ):
        st.balloons()
        st.toast(":rainbow[THANKS FOR DOWNLOADING]")

    done_editing = st.button("DONE EDITING")

    if done_editing:
        st.balloons()
        st.toast(":rainbow[CONGRATULATIONS ON EDITING THE IMAGE]")
        st.snow()

    st.subheader(":green[### INTRODUCING AI CORNER ###]")

    with st.expander(":red[KNOW MORE ABOUT THIS SECTION]"):
        st.write(":orange[***THIS SECTION IS AN EXPERIMENTAL PART WHERE YOU CAN INTERACT WITH THE IMAGE USING AI, ASK ABOUT SUGGESTIONS FOR EDITING, OR GET MORE ABOUT THE UPLOADED IMAGE***]")
        st.caption(":red[***REMEMBER THIS IS TOTALLY EXPERIMENTAL...***]")
        st.caption(":blue[***THANKS TO GEMINI GOOGLE***]")

    # Explanation for the first button
    st.write(":violet[### Ask AI for Suggestions]")
    st.write(":blue[Click the button below to get AI suggestions for editing the uploaded image.]")
    generate = st.button("AI SUGGESTIONS ABOUT EDITING THE IMAGE")

    st.subheader(":red[___OR___]")  
    # Explanation for the custom prompt
    st.write(":orange[### Custom Prompt area]")
    cust_prompt = st.text_input(":blue[Enter your custom query here (Remember to be ethical)]")
    if cust_prompt:
        st.toast(":red[Now click on the generate button]")
    st.markdown(":violet[Click the button below to generate a response based on your custom query.]")
    custom_prompt = st.button("Generate Custom Prompt")
    st.markdown("## PromptGenerationArea")


    # Action when the first button is clicked
    if generate:
        with st.spinner(":rainbow[PLEASE WAIT WHILE THE IMAGE IS BEING EXAMINED....]"):
            
            st.write_stream(image_prompter(image, "Give me suggestions for editing this image"))

    # Action when the custom prompt button is clicked
    if custom_prompt:
        with st.spinner(":rainbow[PLEASE BE PATIENT WHILE THE IMAGE AND YOUR QUERY IS BEING EXAMINED!]"):
            
            if cust_prompt:
                st.write_stream(image_prompter(image, cust_prompt))
            else:
                st.error(":violet[Please enter a custom prompt.]")
                st.write_stream(image_prompter(image, cust_prompt))
            







    
    
        
else:
    st.toast(":red[Upload an image file to start editing.]")
    time.sleep(5)
    st.toast(":red[Upload an image file to start editing.]")
