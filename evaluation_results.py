import streamlit as st
import plotly.graph_objs as go
import numpy as np
from PIL import Image
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class PerformanceData:
    exact_match_rate: float
    average_match_percentage: float
    image_path: str
    title: str
    notes: Optional[str] = None

class PerformanceMetricsVisualizer:
    def __init__(self):
        self.setup_page_header()
    
    @staticmethod
    def setup_page_header():
        st.title("Performance Metrics")
        st.write("all evaluations performed using 100 iterations")
        st.write("Exact match means all parameters perfectly match expected output.")
        st.write("- Ex. Province of Massachusetts and Massachusetts would score negatively")
        st.write("Average match means parameters have acceptable overlap.")
        st.write("- Ex. Province of Massachusetts and Massachusetts would score positively")
    
    @staticmethod
    def create_percentage_plot(subheader: str, match_rate: float) -> go.Figure:
        """Create a gauge chart for displaying match rates."""
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
        """Display metrics for a single document."""
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