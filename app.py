from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image 
from google import genai
from google.genai import types



st.title("🤖📸 Pic2Page AI")
st.subheader("Smart Image & PDF Analyzer")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
uploaded_files = st.file_uploader(
    "Choose Image(s) or PDF",
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=True
)

prompt = st.text_input("Enter your prompt:")


if uploaded_files and st.button("Response"):

    for file in uploaded_files:

        st.divider()
        display_name = file.name

        if len(display_name) > 20:
            display_name = display_name[:20] + "..."

        # st.subheader(f"📁 {display_name}.img")
        

        # -------- IMAGE -------- #
        
        if file.type.startswith("image"):
            image = Image.open(file)
            
            st.image(image, caption=display_name +".img", use_container_width=True)

            contents = [prompt, image]

        # -------- PDF -------- #
        elif file.type == "application/pdf":

            st.info("📄 PDF Uploaded")

            pdf_bytes = file.read()

            pdf_part = types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf"
            )
            

            contents = [prompt, pdf_part]

        # -------- GEMINI RESPONSE -------- #
        with st.spinner(f"Analyzing {display_name}..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )

        st.success("Analysis Completed")
        st.markdown(response.text)