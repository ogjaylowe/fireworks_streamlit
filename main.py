import fireworks.client
import base64
import streamlit as st
from PIL import Image
import json
from dotenv import load_dotenv
import os

# Load env values
load_dotenv()
fireworks.client.api_key = os.getenv('FIREWORKS_API_KEY')

## DEFINITIONS
class KYCDocumentProcessor:
    def __init__(self, response_pattern="", system_prompt="", model="accounts/fireworks/models/phi-3-vision-128k-instruct"):
        """
        Initialize the KYC Document Processor with a specific vision model.
        
        :param model: The vision model to use for document processing
        """
        self.model = model
        
        # Default response pattern template
        self.response_pattern = response_pattern
        
        # Default system prompt for KYC processing
        self.system_prompt = system_prompt

        # Store base64 encoded images and extention for reuse
        self.image_base64 = None
        self.ext = None
    
    def process_document(self, uploaded_image=None, user_prompt=""):
        """
        Process a document image and extract key information.
        
        :param uploaded_image: Path to the image file
        :param image_base64: Base64 encoded image
        :param user_prompt: Optional custom prompt to override default
        :return: Extracted document information
        """
        # No image or referencable encoded image to use
        if not (uploaded_image or self.image_base64):
            raise ValueError("a streamlit uploaded image must be provided")
        
        # process an image whenever provided (supercedes existing data)
        elif (uploaded_image):
            # Read the file contents
            image_bytes = uploaded_image.getvalue()
            
            # Base64 encode the image and assign to self
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            self.image_base64 = image_base64

            # Get file extention type and assign to self
            ext = uploaded_image.name.split('.')[-1]

            # Ensure that image meets extention requirements
            valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'ppm']
            if ext not in valid_extensions:
                raise ValueError(f"Invalid image file extension. Accepted types are: {', '.join(valid_extensions)}")
    
            self.ext = ext
                    
        # Make API call
        try:
            response = fireworks.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": self.system_prompt
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{self.ext};base64,{self.image_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            # Extract and return content
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error processing document: {e}")
            return None

    def update_prompts(self, response_pattern="", system_prompt=""):
        """
        update prompts so that base64 encoded imagery can be reused
        """
        self.response_pattern = response_pattern
        self.system_prompt = system_prompt

## MAIN
def main():
    st.title("Fireworks ai example")

    # Create file uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Check if file is uploaded
    if uploaded_file is not None:

        # Ensure image meets size requirements
        file_size = uploaded_file.size      # Size in bytes
        max_size = 5 * 1024 * 1024          # 5 MB limit
    
        if file_size > max_size:
            st.error(f"Image file is too large. Maximum size is 5 MB.")

        # Open the image using PIL
        image = Image.open(uploaded_file)
        
        # Display the uploaded image
        st.image(image, caption='Uploaded Image', use_container_width=True)

        # Create prompts and a processor object for the document
        response_pattern = {
            "document_type": "passport or drivers_licence",
            "state": "if drivers licence, the state it's from, otherwise None"
        }
        system_prompt = "You are working with a financial services industry (FSI) enterprise account for their know your customer (KYC) process. You will be given Identity Verification documents and must determine if it is an American drivers licence or passport"
        user_prompt = f"Is this Identity Verification document a drivers licence or passport? Return response in the following format: {response_pattern}"
        processor = KYCDocumentProcessor(response_pattern, system_prompt)
        
        # Determine if passport or drivers licence
        passport_or_drivers_licence_response = processor.process_document(uploaded_image=uploaded_file, user_prompt=user_prompt)

        # Convert result into a json object
        passport_or_drivers_licence_response = json.loads(passport_or_drivers_licence_response.replace("'", '"'))
        st.write(passport_or_drivers_licence_response)

        if passport_or_drivers_licence_response["document_type"] == "passport":
            # Update response pattern and prompts for passport processing
            response_pattern = {
                "LN": "Doe",
                "FN": "John",
                "NATIONALITY": "USA",
                "POB": "CALIFORNIA",
                "EXP": "01/01/2020",
                "DOB": "01/01/2020",
            }
            system_prompt = "You are working with a financial services industry (FSI) enterprise account for their know your customer (KYC) process. You will be given Identity Verification documents in the form of travel Passports and must extract information such as name and date of birth (DOB) customer."
            user_prompt = f"what is the surname last name (LN), given first name (FN) which may contain two first names such as Janice Ann or John Q, nationality, place of birth (POB), date of birth (DOB), and date of expiration (DOE) provided by the user? The date of birth and expiration must be in a numerical format such as 01/01/2020. Provide you answer in the following format: {response_pattern}. Disregard all other information not in the response pattern."

            processor.update_prompts(response_pattern, system_prompt)
            passport_data = processor.process_document(user_prompt=user_prompt)
            passport_data = json.loads(passport_data.replace("'", '"'))
            st.write(passport_data)
        else:
            response_pattern = {
                "DL": "abcd12345",
                "EXP": "01/01/2020",
                "FN": "John",
                "LN": "Doe",
                "DOB": "01/01/2020"
            }

            system_prompt = "You are working with a financial services industry (FSI) enterprise account for their know your customer (KYC) process. You will be given Identity Verification documents such as Passports & Drivers license and must extract information such as drivers licence number, name, and date of birth (DOB)."
            image_prompt = f"what is the drivers licence (DL) number denoted by the number 1, expiration date (EXP), last name (LN), first name (FN) which may contain two first names such as Janice Ann or John Q, and date of birth (DOB) provided by the user? Provide you answer in the following format: {response_pattern}. Disregard all other information not in the response pattern."
    
            processor.update_prompts(response_pattern, system_prompt)
            drivers_licence_data = processor.process_document(user_prompt=image_prompt)
            drivers_licence_data = json.loads(drivers_licence_data.replace("'", '"'))
            st.write(drivers_licence_data)

pg = st.navigation([st.Page(main), st.Page("eval1.py")])
pg.run()