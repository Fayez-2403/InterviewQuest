import streamlit as st
import pandas as pd
import os
from docx import Document
from bertopic import BERTopic
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim
import matplotlib.pyplot as plt
from PIL import Image
import io
from PIL import ImageOps

def ls(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')

def pp(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 1:
            result.append(ls(token))
    result = ' '.join(result)
    return result

def get_ques_list(folder):
    os.chdir(folder)
    os.chdir('company')
    list_of_files = os.listdir()
    all_ques = {}
    for filename in list_of_files:
        if filename.endswith('.docx'):
            doc = Document(filename)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            doctxt = fullText
            fullText = []
            for eachl in doctxt:
                if len(eachl) == 0:
                    continue
                elif eachl[0] == 'Q':
                    fullText.append(eachl.split(" ", 1)[1])
                else:
                    fullText[len(fullText)-1] = fullText[len(fullText)-1] + ' ' + eachl

            all_ques[filename[:len(filename)-5]] = fullText
    return all_ques

# Function to get topics with mapping
def get_topics_with_mapping(docx_path, model_path='model', num_topics=2, csv_path='mapping.csv'):
    # Get questions list
    ques_list_per_company = get_ques_list(docx_path)
    
    os.chdir('..')
    # Load mapping data from CSV file
    mapping_data = pd.read_csv(csv_path)

    model = BERTopic.load(model_path)

   # Process each question and get topics
    all_topics_per_company = {}
    all_results_table = {}
    for key, value in ques_list_per_company.items():
        ques_list = value
        one_company_topics = []
        results_table = []
        for idx, ques in enumerate(ques_list):
            preprocessed_question = pp(ques)
            similar_topics, _ = model.find_topics(preprocessed_question, top_n=num_topics)

            # Map bucket_topic_number to book_topic_number with the highest non-zero score
            book_topic_number_1, book_topic_number_2 = None, None
            score_1, score_2 = 0.0, 0.0
            for topic_number in similar_topics:
                # Filter the mapping data for the current bucket_topic_number
                topic_data = mapping_data[mapping_data['bucket_topic_number'] == topic_number + 1]
                
                # Get the book_topic_number and corresponding score
                if not topic_data.empty:
                    current_score = topic_data['score'].max()
                    current_book_topic_number = topic_data.loc[topic_data['score'].idxmax()]['book_topic_number']

                    # Assign to variables based on score
                    if current_score >= score_1:
                        score_2, score_1 = score_1, current_score
                        book_topic_number_2, book_topic_number_1 = book_topic_number_1, current_book_topic_number
                    elif current_score >= score_2:
                        score_2 = current_score
                        book_topic_number_2 = current_book_topic_number

            # Get the names of topics
            book_topic_1 = mapping_data[mapping_data['book_topic_number'] == book_topic_number_1]['book_topic'].values[0] if book_topic_number_1 is not None else None
            book_topic_2 = mapping_data[mapping_data['book_topic_number'] == book_topic_number_2]['book_topic'].values[0] if book_topic_number_2 is not None else None

            # Store the topics for the company
            one_company_topics.append((ques, similar_topics, (book_topic_number_1, score_1, book_topic_1), (book_topic_number_2, score_2, book_topic_2)))

            # Store results in a table
            results_table.append({
                'Question': ques,
                'Topics': similar_topics,
                'Book Topic 1': f"{book_topic_number_1} - {book_topic_1} (Score: {score_1})" if book_topic_number_1 is not None else None,
                'Book Topic 2': f"{book_topic_number_2} - {book_topic_2} (Score: {score_2})" if book_topic_number_2 is not None else None
            })

        all_topics_per_company[key] = one_company_topics
        all_results_table[key] = results_table

    os.chdir('..')
    return all_topics_per_company, all_results_table

# Initialize the result variable outside the main function
result = {}
# Function to display data table
def display_data_table(result, results_table, selected_company):
    with st.expander(f"Data for Company {selected_company}"):
        df = pd.DataFrame(results_table[selected_company])
        st.table(df)

# Function to display images
def display_images(docx_path, companies):
    image_folder = os.path.join(docx_path, 'graph')

    for company in companies:
        st.subheader(f"For Company {company}")
        images = [f for f in os.listdir(image_folder) if f.startswith(f'book_topic_frequencies_{company}') and f.endswith('.png')]

        if images:
            for image in images:
                image_path = os.path.join(image_folder, image)

                # Open, transpose, and thumbnail the image with a different resampling filter (e.g., Image.LANCZOS)
                img = Image.open(image_path)
                img = ImageOps.exif_transpose(img)
                img.thumbnail((800, 800), Image.LANCZOS)  # Adjust the size and resampling filter as needed

                # Display the resized image
                st.image(img, caption=f'Book Topic Frequencies - {company}', use_column_width=True)
        else:
            st.warning(f"No images found for {company}.")



# Streamlit app
def main():
    # st.set_page_config(layout="wide")

    # Set the page title    
    st.title("Placement Data Analytics Tool")

    # Get docx_path from user input with reduced input box width
    allowed_inputs = ["Networking", "DBMS", "OperatingSystem"]
    user_input = st.text_input("Enter the path to the folder containing .docx files:")

    # Input validation
    if user_input and user_input not in allowed_inputs:
        st.error("Invalid input. Please enter one of the following: Networking, DBMS, OperatingSystem")
        return

    # Add a sidebar for navigation and user instructions
    st.sidebar.title("Navigation")
    selected_view = st.sidebar.radio("Select View:", ["Data Table", "Images"])

    st.sidebar.markdown(
        """
        **Instructions:**

        - Enter the path to the folder containing .docx files.
        - Click on the "Analyze" button to perform the analysis.
        - Use the sidebar to switch between different views.
        """
    )

    # Get result using the function
    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            try:
                result, results_table = get_topics_with_mapping(user_input)
                companies = list(result.keys())

                if selected_view == "Data Table":
                    # Display data tables with separate expanders for each company
                    # selected_company1 = st.selectbox("Select Company 1:", companies)
                    display_data_table(result, results_table, 'Amazon')

                    # selected_company2 = st.selectbox("Select Company 2:", companies)
                    display_data_table(result, results_table, 'Google')

                    # selected_company3 = st.selectbox("Select Company 3:", companies)
                    display_data_table(result, results_table, 'Microsoft')

                elif selected_view == "Images":
                    # Display images for all companies
                    display_images(user_input, companies)

                st.success("Analysis Completed!")

            except Exception as e:
                st.error(f"Error: {e}")

# Function to display result
# def display_result(result, results_table, docx_path):
#     for company, question_topics_list in result.items():
#         # Create two columns
#         col1, col2 = st.columns(2)

#         # Display the table in the first column
#         table_expander_placeholder = col1.empty()
#         with table_expander_placeholder:
#             table_expander = st.expander(f"Data for Company {company}", expanded=False)
#             df = pd.DataFrame(results_table[company])
#             table_expander.table(df)

#         # Display images for the current company in the second column
#         with col2.expander(f"Images for Company {company}", expanded=True):
#             image_folder = os.path.join(docx_path, 'graph')
#             images = [f for f in os.listdir(image_folder) if f.startswith(f'book_topic_frequencies_{company}') and f.endswith('.png')]

#             if images:
#                 for image in images:
#                     image_path = os.path.join(image_folder, image)

#                     # Open, transpose, and thumbnail the image with different resampling filters
#                     img = Image.open(image_path)
#                     img = ImageOps.exif_transpose(img)
#                     img.thumbnail((800, 800), Image.BICUBIC)  # Experiment with different resampling filters

#                     # Display the resized image
#                     col2.image(img, caption=f'Book Topic Frequencies - {company}', use_column_width=True)
#             else:
#                 col2.warning("No images found for the selected company.")


# # Streamlit app
# def main():
#     st.set_page_config(layout="wide")
#     global result

#     # Set the page title    
#     st.title("Placement Data Analytics Tool")

#     # Get docx_path from user input with reduced input box width
#     allowed_inputs = ["Networking", "DBMS", "OperatingSystem"]
#     user_input = st.text_input("Enter the path to the folder containing .docx files:")

#     # Input validation
#     if user_input and user_input not in allowed_inputs:
#         st.error("Invalid input. Please enter one of the following: Networking, DBMS, OperatingSystem")
#         return

#     st.markdown("""<style>div[data-baseweb="input"] { width: 300px; }</style>""", unsafe_allow_html=True)

#     # Create an empty container for the button
#     button_container = st.empty()

#     # Get result using the function
#     if button_container.button("Analyze"):
#         with st.spinner("Analyzing..."):
#             try:
#                 result, results_table = get_topics_with_mapping(user_input)

#                 # Display result
#                 display_result(result, results_table, user_input)

#                 st.success("Analysis Completed!")

#             except Exception as e:
#                 st.error(f"Error: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
