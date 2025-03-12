from dotenv import load_dotenv

# Load environment variables (like API keys) from .env file
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the Gemini API with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to call Google Gemini API and get the generated response based on the image and prompt
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')  # Use Gemini Pro model for analysis
    response = model.generate_content([input, image[0], prompt])  # Send the prompt, image, and input to the model
    return response.text  # Return the generated response (text)

# Function to process the uploaded image and return it in a format for Gemini API
def input_image_setup(uploaded_file):
    # Check if an image has been uploaded
    if uploaded_file is not None:
        # Read the image file into bytes
        bytes_data = uploaded_file.getvalue()

        # Format the image into a structure that Gemini API expects
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type (e.g., image/jpeg, image/png)
                "data": bytes_data  # Pass the image bytes data
            }
        ]
        return image_parts  # Return the image formatted for API
    else:
        raise FileNotFoundError("No file uploaded")  # Raise error if no file is uploaded

# Initialize the Streamlit app and set the page title
st.set_page_config(page_title="NutriVision")

# Display the main header for the app
st.title("Nutrient Breakdown & Health Insights System")

# Display the subheader, which shows the developer's name
st.subheader("Developed by Emon Hasan")

# File uploader allows users to upload a food image
uploaded_file = st.file_uploader("Upload an image of food", type=["jpg", "jpeg", "png"])

# Initialize an empty image variable
image = ""

# Check if a file is uploaded and display the image
if uploaded_file is not None:
    image = Image.open(uploaded_file)  # Open the uploaded image
    st.image(image, caption="Uploaded Image", use_container_width=True)  # Display the image in Streamlit

# A button to trigger the food analysis
submit = st.button("Analyze Food")

# Nutritionist prompt: Detailed instructions for the AI model to analyze food
nutrition_prompt = """
You are a highly skilled AI nutritionist. Analyze the food items in the provided image 
and generate a **comprehensive nutritional breakdown** including:

✅ **Food Category** (e.g., Fruit, Vegetable, Meat, Dairy, Processed Food, etc.)  
✅ **Total Calories**  
✅ **Macronutrients** (Carbohydrates, Proteins, Fats):  
   - Carbohydrates (g)  
   - Proteins (g)  
   - Fats (g)  
✅ **Micronutrients** (All Vitamins & Minerals):  
   - Vitamin A, B, C, D, E, K  
   - Iron, Calcium, Zinc, Magnesium, Potassium, etc.  
✅ **Dietary Fiber & Sugar** (in grams)  
✅ **Sodium Levels** (mg) – Indicate if it's safe or too high  
✅ **Health Benefits & Warnings**  
   - ✅ Good nutrients & how they help (e.g., "High in Vitamin C, boosts immunity")  
   - ⚠️ Warnings (e.g., "High sodium, not recommended for hypertension")  

### Output Format Example:
----------------------------------------------------------
🍽 **Food Item 1 (Name & Category)**  
- **Calories**: X kcal  
- **Carbohydrates**: Y g  
- **Proteins**: Z g  
- **Fats**: W g  
- **Vitamins & Minerals**:  
   - Vitamin A: X mcg  
   - Vitamin C: Y mg  
   - Iron: Z mg  
   - Calcium: W mg  
- **Sugar & Fiber**:   
   - Dietary Fiber: X g  
   - Sugar: Y g  
- **Sodium Level**: X mg (Safe / High Warning 🚨)  
- **Health Benefits**:  
   - ✅ Supports immune system  
   - ✅ Good for digestion  
- **Warnings**:  
   - ⚠️ High sodium, not recommended for heart patients  
----------------------------------------------------------
🍽 **Food Item 2**  
(Same structured analysis for each food item detected)

### After analyzing all items, provide the **total nutritional values**:
- **Total Calories**: X kcal  
- **Total Carbohydrates**: Y g  
- **Total Proteins**: Z g  
- **Total Fats**: W g  
- **Total Vitamins & Minerals**:  
   - Vitamin A: X mcg  
   - Vitamin C: Y mg  
   - Iron: Z mg  
   - Calcium: W mg  
- **Total Sugar & Fiber**:  
   - Dietary Fiber: X g  
   - Sugar: Y g  
- **Total Sodium Level**: X mg

### **Overall Health Benefits**:
- Based on the overall nutritional intake, please provide health benefits like:
   - Weight loss benefits
   - Heart health
   - Bone health support
   - Immune system strengthening

### **Overall Health Warnings**:
- Based on the overall nutritional intake, please provide any health warnings:
   - ⚠️ High sodium levels (if applicable)
   - ⚠️ High sugar intake (if applicable)
   - ⚠️ High cholesterol (if applicable)
   - ⚠️ Not recommended for diabetes or heart patients (if applicable)

Provide **accurate and detailed nutritional information** based on real-world data for each item and totals for the entire meal.
"""

## When the submit button is clicked
if submit:
    if uploaded_file is not None:
        # Process the image and send it to Gemini for analysis
        image_data = input_image_setup(uploaded_file)  # Prepare the image for the API
        response = get_gemini_response("Analyze this food image", image_data, nutrition_prompt)  # Get AI's response
        
        # Display the nutritional analysis response from Gemini
        st.subheader("Food Nutritional Analysis")  
        st.write(response)  # Show the response text in the app
    else:
        st.warning("Please upload an image before submitting.")  # Display a warning if no image is uploaded