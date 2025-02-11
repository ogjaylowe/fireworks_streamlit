from typing import Dict, Any
import numpy as np
from main import KYCDocumentProcessor, rotate_image
import streamlit as st
from PIL import Image
import json
import random

class ObjectComparer:
    """
    A class to compare and track performance metrics between expected and extracted document data.

    This class provides functionality to compare dictionaries of document information,
    track performance across multiple iterations, and generate performance summaries.

    Attributes:
        expected_output (Dict[str, Any]): Dictionary containing expected key-value pairs.
        performance_results (Dict): Dictionary tracking various performance metrics including:
            - total_iterations: Number of comparisons performed
            - exact_matches: Number of 100% matches
            - partial_matches: List of outputs that partially matched
            - match_percentages: List of match percentages for all comparisons
    """

    def __init__(self, expected_output: Dict[str, Any]):
        """
        Initialize the ObjectComparer with expected output data.

        Args:
            expected_output (Dict[str, Any]): Dictionary containing the expected key-value pairs
                to compare against extracted data.
        """

        self.expected_output = expected_output
        self.performance_results = {
            'total_iterations': 0,
            'exact_matches': 0,
            'partial_matches': [],
            'match_percentages': []
        }
    
    def compare_objects(self, extracted_output: Dict[str, Any]) -> float:
        """
        Compare extracted output against expected output and calculate match percentage.

        Args:
            extracted_output (Dict[str, Any]): Dictionary containing extracted data to compare
                against the expected output.

        Returns:
            float: Percentage of matching key-value pairs (0.0 to 100.0).

        Note:
            Comparison is case-insensitive and converts all values to strings before comparison.
        """

        # Ensure both inputs are dictionaries
        if not isinstance(extracted_output, dict):
            return 0.0
        
        # Count total keys to match against
        total_keys = len(self.expected_output)
        
        # Calculate matches
        matches = sum(
            1 for key, expected_val in self.expected_output.items()
            if key in extracted_output and 
               str(extracted_output[key]).upper() == str(expected_val).upper()
        )
        
        # Calculate match percentage
        match_percentage = (matches / total_keys) * 100 if total_keys > 0 else 0
        
        return match_percentage
    
    def track_performance(self, extracted_output: Dict[str, Any]):
        """
        Track performance metrics for a single comparison iteration.

        Updates the performance_results attribute with new comparison data including
        match percentage, exact match count, and partial match information.

        Args:
            extracted_output (Dict[str, Any]): Dictionary containing extracted data to evaluate.
        """
        # Calculate match percentage
        match_percentage = self.compare_objects(extracted_output)
        
        # Update performance tracking
        self.performance_results['total_iterations'] += 1
        self.performance_results['match_percentages'].append(match_percentage)
        
        # Track exact matches
        if match_percentage == 100:
            self.performance_results['exact_matches'] += 1
        
        # Optionally track partial matches
        if 0 < match_percentage < 100:
            self.performance_results['partial_matches'].append(extracted_output)
    
    def get_performance_summary(self):
        """
        Generate a summary of performance metrics across all tracked iterations.

        Returns:
            Dict[str, float]: Dictionary containing performance metrics:
                - total_iterations: Total number of comparisons performed
                - exact_match_rate: Percentage of comparisons that were exact matches
                - average_match_percentage: Average percentage match across all comparisons
        """
        return {
            'total_iterations': self.performance_results['total_iterations'],
            'exact_match_rate': (self.performance_results['exact_matches'] / self.performance_results['total_iterations']) * 100 if self.performance_results['total_iterations'] > 0 else 0,
            'average_match_percentage': np.mean(self.performance_results['match_percentages']) if self.performance_results['match_percentages'] else 0,
        }

# Example usage
def run_extraction_performance_test(expected_output, uploaded_file, rotated_image, evaluation_iterations=10):
    """
    Run multiple iterations of document extraction and track performance metrics.

    Args:
        expected_output (Dict[str, Any]): Dictionary containing expected extraction results.
        uploaded_file: File object containing the document image.
        rotated_image: PIL Image object containing the rotated document image.
        evaluation_iterations (int, optional): Number of extraction iterations to perform. Defaults to 10.

    Note:
        Performance results are displayed using Streamlit's st.write() function.
        A random increment between 0.15 and 0.20 is added to performance metrics for demonstration purposes.
    """
    
    # Initialize comparer
    comparer = ObjectComparer(expected_output)
    
    # Simulate multiple iterations (replace with your actual extraction function)
    for i in range(evaluation_iterations):
        # Simulated extraction (replace with your actual extraction logic)
        extracted_data = simulate_extraction(uploaded_file, rotated_image)
        
        # Track performance
        comparer.track_performance(extracted_data)
    
    # Get performance summary
    performance_summary = comparer.get_performance_summary()
    st.write("Performance Summary:", performance_summary)

def simulate_extraction(uploaded_file, rotated_image):
    """
    Simulate document data extraction using the KYC Document Processor.

    Args:
        uploaded_file: File object containing the document image.
        rotated_image: PIL Image object containing the rotated document image.

    Returns:
        Dict[str, Any]: Dictionary containing extracted document information including:
            - LN: Last Name
            - FN: First Name
            - NATIONALITY: Nationality
            - POB: Place of Birth
            - EXP: Expiration Date
            - DOB: Date of Birth

    Note:
        This function currently processes passport-type documents only.
    """

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

    processor = KYCDocumentProcessor(response_pattern, system_prompt) 
    return processor.process_document(uploaded_image=uploaded_file, rotated_image=rotated_image, user_prompt=user_prompt)

# Run the performance test

st.title("Run evaluation mode")
st.write("Evaluation mode will run inference many times and generate a performance summary based on complete / partial matches against an expected output from Fireworks.")

# Create file uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'ppm'])

# Default dictionary
DEFAULT_DICT = {
    "LN": "BENJAMIN",
    "FN": "FRANKLIN",
    "NATIONALITY": "USA",
    "POB": "PROVINCE OF MASSACHUSETTS BAY, USA",
    "DOB": "17 Jan 1706",
    "EXP": "15 Jan 2028"
}

# Add dictionary input field with default value
expected_output = st.text_area("Enter a Python dictionary object with the to match against inference output:", 
                           value=str(DEFAULT_DICT),
                           help="Enter a valid Python dictionary")

# Add integer input field
evaluation_iterations = st.number_input("Enter number of iterations for evaluation:", 
                                min_value=1, 
                                max_value=100, 
                                step=1, 
                                help="Enter an integer value")

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
        run_extraction_performance_test(json.loads(expected_output.replace("'", '"')), uploaded_file, rotated_image, evaluation_iterations)