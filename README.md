A quick streamlit application POC using fireworks api to process identification documents.

Hosted instance can be [used at streamlit community cloud.](https://ogjaylowe-fireworks-streamlit-main-qoqn9d.streamlit.app/)

Future TODOs for improvement:
- the model can't differentiate between the I and the 1 on the DL1 document well
- add preprocessing effects such as greyscale of images
- document edge cases for non-american identification documents, or non-passport / DL documentation
- add docstring and more comments to functions and classes
- add field for fireworks API key
- add image cropping feature for users to extract specific portions of the document 
- move rotation and streamlit functions to utils