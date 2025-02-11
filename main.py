import fireworks.client
import base64
import streamlit as st
from PIL import Image
import json
from dotenv import load_dotenv
import os
import io

# Load env values
load_dotenv()
fireworks.client.api_key = os.getenv('FIREWORKS_API_KEY')

## DEFINITIONS
class KYCDocumentProcessor:
    """
    A class to process KYC (Know Your Customer) documents using vision AI models.

    This class handles the processing of identity documents like passports and driver's licenses,
    converting them to base64 format and sending them to a vision model for information extraction.

    Attributes:
        model (str): The vision model identifier to use for document processing.
        response_pattern (str): Template for structuring the response output.
        system_prompt (str): System-level prompt for the vision model.
        image_base64 (str): Base64 encoded image data.
        ext (str): File extension of the processed image.
    """

    def __init__(self, response_pattern="", system_prompt="", model="accounts/fireworks/models/phi-3-vision-128k-instruct"):
        """
        Initialize the KYC Document Processor with specified parameters.

        Args:
            response_pattern (str, optional): Template for structuring the response. Defaults to empty string.
            system_prompt (str, optional): System-level prompt for the vision model. Defaults to empty string.
            model (str, optional): Vision model identifier. Defaults to "accounts/fireworks/models/phi-3-vision-128k-instruct".
        """
        self.model = model
        
        # Default response pattern template
        self.response_pattern = response_pattern
        
        # Default system prompt for KYC processing
        self.system_prompt = system_prompt

        # Store base64 encoded images and extention for reuse
        self.image_base64 = None
        self.ext = None
    
    def process_document(self, uploaded_image=None, rotated_image=None, user_prompt="", doc_type=False):
        """
        Process a document image and extract key information.

        Args:
            uploaded_image (StreamlitUploadedFile, optional): The uploaded image file. Defaults to None.
            rotated_image (PIL.Image, optional): A rotated version of the image. Defaults to None.
            user_prompt (str, optional): Custom prompt for the vision model. Defaults to empty string.
            doc_type (Union[bool, list], optional): Document types to filter for. Defaults to False.

        Returns:
            dict: Extracted document information in JSON format.

        Raises:
            ValueError: If no image is provided or if the image format is invalid.
            RuntimeError: If document processing fails after maximum attempts.
        """
        # No image or referencable encoded image to use
        if not (uploaded_image or self.image_base64):
            raise ValueError("a streamlit uploaded image must be provided")
        
        # process an image whenever provided (supercedes existing data)
        elif (uploaded_image):
            # Read the file contents
            # Create a bytes buffer
            buffered = io.BytesIO()
            
            # Save the rotated pillow image to the buffer
            rotated_image.save(buffered, format="PNG")
            
            # Get the byte values from the rotated image and encode to base64
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            self.image_base64 = image_base64

            # Get file extention type and assign to self
            ext = uploaded_image.name.split('.')[-1]

            # Ensure that image meets extention requirements
            valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'ppm']
            if ext not in valid_extensions:
                raise ValueError(f"Invalid image file extension. Accepted types are: {', '.join(valid_extensions)}")
    
            self.ext = ext
                    
        # Make API call
        max_attempts = 5
        for attempt in range(max_attempts):
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
                passport_or_driver_licence_response = json.loads(response.choices[0].message.content.replace("'", '"'))
                st.write(passport_or_driver_licence_response)

                if not doc_type:
                    return passport_or_driver_licence_response
                elif any(i in passport_or_driver_licence_response["document_type"] for i in doc_type):
                    return passport_or_driver_licence_response

            except Exception as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Failed to process document after {max_attempts} attempts: {str(e)}")

    def update_prompts(self, response_pattern="", system_prompt=""):
        """
        Update the response pattern and system prompt for reusing base64 encoded images.

        Args:
            response_pattern (str, optional): New response pattern template. Defaults to empty string.
            system_prompt (str, optional): New system-level prompt. Defaults to empty string.
        """
        self.response_pattern = response_pattern
        self.system_prompt = system_prompt

def rotate_image(image, rotation):
    """
    Rotate an image by a specified number of degrees.

    Args:
        image (PIL.Image): Input image to be rotated.
        rotation (int): Rotation angle in degrees. Must be one of [0, 90, 180, 270, 360].

    Returns:
        PIL.Image: Rotated image.

    Note:
        If an invalid rotation angle is provided, returns the original image and displays a warning.
    """
    # Ensure rotation is one of the valid increments
    valid_rotations = [0, 90, 180, 270, 360]
    if rotation not in valid_rotations:
        st.warning(f"Invalid rotation. Choose from {valid_rotations}")
        return image
    
    # Rotate the image
    return image.rotate(rotation)

## MAIN
def main():
    st.title("Fireworks ai example")
    st.write("Process a single indentification document using a two step process (document type classification -> data extraction) and get an output containing information regarding it")
    st.write("No data is saved in this app so feel free to use any documents you want. Sample imagery can be found for testing on the evaluation results tab.")
    st.write("The API key is metered so don't go crazy on it with evaluation mode!")
    
    # Create file uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'ppm'])

    # Check if file is uploaded
    if uploaded_file is not None:

        # Ensure image meets size requirements
        file_size = uploaded_file.size      # Size in bytes
        max_size = 5 * 1024 * 1024          # 5 MB limit
    
        if file_size > max_size:
            st.error(f"Image file is too large. Maximum size is 5 MB.")

        # Open the image using PIL
        image = Image.open(uploaded_file)
        
        # Rotation selection
        rotation = st.select_slider(
            'Rotate Image',
            options=[0, 90, 180, 270, 360],
            value=0
        )
        
        # Rotate the image
        rotated_image = rotate_image(image, rotation)
        
        # Display original and rotated images
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Original Image")
            st.image(image)
        
        with col2:
            st.header("Rotated Image")
            st.image(rotated_image)
        
        # Option to process rotated image further
        if st.button("Process rotated image or regenerate response"):
            st.write("Processing rotated image...")

            # Create prompts and a processor object for the document
            response_pattern = {
                "document_type": "passport or driver_licence",
                "state": "if drivers licence, the state it's from, otherwise None"
            }
            system_prompt = "You are working with a financial services industry (FSI) enterprise account for their know your customer (KYC) process. You will be given Identity Verification documents and must determine if it is an American drivers licence or passport"
            user_prompt = f"Is this Identity Verification document a drivers licence or passport? Return response in the following format: {response_pattern}"
            
            processor = KYCDocumentProcessor(response_pattern, system_prompt)
            # processor = KYCDocumentProcessor(response_pattern, system_prompt, model="accounts/fireworks/models/llama-v3p2-90b-vision-instruct")
            
            passport_or_driver_licence_response = processor.process_document(uploaded_image=uploaded_file, rotated_image=rotated_image, user_prompt=user_prompt, doc_type=["passport", "driver_licence"])

            if passport_or_driver_licence_response["document_type"] == "passport":
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
                processor.process_document(user_prompt=user_prompt)
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
                processor.process_document(user_prompt=image_prompt)

pg = st.navigation([st.Page(main), st.Page("run_evaluation.py"), st.Page("evaluation_results.py")])
pg.run()