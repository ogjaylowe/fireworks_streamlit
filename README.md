A streamlit application using fireworks api to process identification documents.

TODOs:
# TODO - make an evaluation function that compares the answers to a json object 100 times -> chart results in seperate pages
# TODO - the model can't differentiate between the I and the 1 on the DL
# TODO - preprocessing of images?
# TODO - document edge cases for non-american identification documents, or non-passport / DL documentation
# TODO - for each iteration, make a new page

add docstring stuff to functions and classes
add field for fireworks API key
add image cropping feature 
move rotation stuff to utils?


Performance Summary: {'total_iterations': 10, 'exact_match_rate': 0.0, 'average_match_percentage': np.float64(45.0), 'match_percentage_std_dev': np.float64(13.017082793177757)}