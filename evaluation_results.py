import streamlit as st
import plotly.graph_objs as go
import numpy as np
from PIL import Image
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class PerformanceData:
    """
    Data class representing performance metrics and metadata for a document.

    Attributes:
        exact_match_rate (float): Rate of exact matches (0.0 to 1.0).
        average_match_percentage (float): Average percentage of matches (0.0 to 100.0).
        image_path (str): File path to the document image.
        title (str): Display title for the document.
        notes (Optional[str]): Additional notes about the document performance, if any.
    """

    exact_match_rate: float
    average_match_percentage: float
    image_path: str
    title: str
    notes: Optional[str] = None

class PerformanceMetricsVisualizer:
    """
    A class for visualizing document processing performance metrics using Streamlit.

    This class provides functionality to create and display performance visualizations
    including gauge charts and document images in a structured layout.
    """

    def __init__(self):
        """
        A class for visualizing document processing performance metrics using Streamlit.

        This class provides functionality to create and display performance visualizations
        including gauge charts and document images in a structured layout.
        """
        self.setup_page_header()
    
    @staticmethod
    def setup_page_header():
        """
        Set up the Streamlit page header with title and explanatory text.

        Displays information about:
        - Number of iterations used in evaluations
        - Definition of exact matches
        - Definition of average matches
        """

        st.title("Performance Metrics")
        st.write("all evaluations performed using 100 iterations")
        st.write("Exact match means all parameters perfectly match expected output.")
        st.write("- Ex. Province of Massachusetts and Massachusetts would score negatively")
        st.write("Average match means parameters have acceptable overlap.")
        st.write("- Ex. Province of Massachusetts and Massachusetts would score positively")
    
    @staticmethod
    def create_percentage_plot(subheader: str, match_rate: float) -> go.Figure:
        """
        Create a gauge chart visualization for displaying match rates.

        Args:
            subheader (str): Title text for the gauge chart.
            match_rate (float): Match rate value to display (0.0 to 100.0).

        Returns:
            go.Figure: Plotly figure object containing the gauge chart.

        Note:
            The gauge is color-coded with:
            - Red for values 0-50
            - Green for values 50-100
            - Blue indicator bar
        """

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=match_rate,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': subheader},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightcoral"},
                    {'range': [50, 100], 'color': "lightgreen"}
                ]
            }
        ))
        fig.update_layout(height=300)
        return fig
    
    def display_metrics(self, performance_data: PerformanceData):
        """
        Display performance metrics and document image in a three-column layout.

        Args:
            performance_data (PerformanceData): Performance metrics and metadata for a document.

        Layout:
            - Column 1: Document image
            - Column 2: Exact match percentage gauge chart
            - Column 3: Average match percentage gauge chart
        """

        st.subheader(performance_data.title)
        if performance_data.notes:
            st.write(performance_data.notes)
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            image = Image.open(performance_data.image_path)
            st.image(image, width=300)
        
        with col2:
            st.plotly_chart(
                self.create_percentage_plot(
                    "Exact Match %",
                    performance_data.exact_match_rate * 100
                )
            )
            
        with col3:
            st.plotly_chart(
                self.create_percentage_plot(
                    "Average Match %",
                    performance_data.average_match_percentage
                )
            )

def main():
    """
    Main function to initialize and run the performance metrics visualization.

    Creates sample performance data for multiple documents and displays their
    metrics using the PerformanceMetricsVisualizer.

    Document types include:
    - Driver licenses (3 samples)
    - Passports (2 samples)
    """
    
    # Define performance data for all documents
    documents = [
        PerformanceData(
            exact_match_rate=0.22,
            average_match_percentage=87.0,
            image_path="test_imagery/License 1.png",
            title="Driver License 1"
        ),
        PerformanceData(
            exact_match_rate=0.31,
            average_match_percentage=93.0,
            image_path="test_imagery/License-2.jpg",
            title="Driver License 2"
        ),
        PerformanceData(
            exact_match_rate=0.18,
            average_match_percentage=78.0,
            image_path="test_imagery/License-3.jpeg",
            title="Driver License 3",
            notes="after rotation"
        ),
        PerformanceData(
            exact_match_rate=0.26,
            average_match_percentage=96.0,
            image_path="test_imagery/passport-1.jpeg",
            title="Passport 1"
        ),
        PerformanceData(
            exact_match_rate=0.21,
            average_match_percentage=95.0,
            image_path="test_imagery/passport-2.jpg",
            title="Passport 2",
            notes="after rotation"
        )
    ]
    
    # Initialize visualizer and display all documents
    visualizer = PerformanceMetricsVisualizer()
    for doc in documents:
        visualizer.display_metrics(doc)

if __name__ == "__main__":
    main()