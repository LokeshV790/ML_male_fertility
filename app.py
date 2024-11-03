import streamlit as st
import numpy as np
import tensorflow as tf
from utils.input_processing import update_inputs
from utils.recommendations import provide_recommendations
from utils.translations import translations  # Import translations

# Load the trained model
model = tf.keras.models.load_model('model/fertitlity_dn.h5')

# Language selection
language = st.selectbox("Select Language", ['English', 'हिन्दी', 'ಕನ್ನಡ', 'ગુજરાતી', 'मराठी', 'বাংলা', 'தமிழ்', 'తెలుగు', 'മലയാളം', 'ਪੰਜਾਬੀ'])
lang_key = {
    'English': 'en',
    'हिन्दी': 'hi',
    'ಕನ್ನಡ': 'kn',
    'ગુજરાતી': 'gu',
    'मराठी': 'mr',
    'বাংলা': 'bn',
    'தமிழ்': 'ta',
    'తెలుగు': 'te',
    'മലയാളം': 'ml',
    'ਪੰਜਾਬੀ': 'pa'
}.get(language, 'en')  # Default to English if no match found
lang_dict = translations[lang_key]

# Set title and optional logo
st.title(lang_dict["title"])
# st.image('assets/logo.png', width=200)  # Uncomment and replace with logo path if available

# Use columns for layout
col1, col2 = st.columns(2)
with col1:
    diseases = st.selectbox(lang_dict["childhood_diseases"], ['Yes', 'No'])
    accident = st.selectbox(lang_dict["accident"], ['Yes', 'No'])
    surgery = st.selectbox(lang_dict["surgery"], ['Yes', 'No'])

with col2:
    fever = st.selectbox(lang_dict["fever"], ['Fever < 3 Months (-1)', 'Fever > 3 Months (0)', 'No Fever (1)'], 
                         on_change=update_inputs, args=("fever", "fever"))
    alcohol = st.selectbox(lang_dict["alcohol"], ['Several Times a Day (0.2)', 'Every Day (0.4)', 
                                                 'Several Times a Week (0.6)', 'Once a Week (0.8)', 
                                                 'Hardly Ever (1.0)'], 
                           on_change=update_inputs, args=("alcohol", "alcohol"))

# Additional inputs in columns
st.write("---")  # Divider line for clarity
col3, col4 = st.columns(2)
with col3:
    smoking = st.selectbox(lang_dict["smoking"], ['Never (-1)', 'Occasionally (0)', 'Daily (1)'],
                           on_change=update_inputs, args=("smoking", "smoking"))
    sitting = st.selectbox(lang_dict["sitting"], ['0-8 hours', '9-16 hours'], 
                           on_change=update_inputs, args=("sitting", "sitting"))

with col4:
    season = st.selectbox(lang_dict["season"], ['Winter (-1)', 'Spring (-0.33)', 'Summer (0.33)', 'Fall (1)'],
                          on_change=update_inputs, args=("season", "season"))
    age = st.selectbox(lang_dict["age"], ['27 Years or Under (0.5)', 'Over 27 Years (1.0)'],
                       on_change=update_inputs, args=("age", "age"))

# Prepare input for the model
input_data = np.array([
    1 if diseases == 'Yes' else 0,
    1 if accident == 'Yes' else 0,
    1 if surgery == 'Yes' else 0,
    st.session_state.get('fever_neg1', 0),
    st.session_state.get('fever_0', 0),
    st.session_state.get('fever_1', 0),
    st.session_state.get('alcohol_0.2', 0),
    st.session_state.get('alcohol_0.4', 0),
    st.session_state.get('alcohol_0.6', 0),
    st.session_state.get('alcohol_0.8', 0),
    st.session_state.get('alcohol_1.0', 0),
    st.session_state.get('smoking_-1', 0),
    st.session_state.get('smoking_0', 0),
    st.session_state.get('smoking_1', 0),
    st.session_state.get('sitting_0.5', 0),
    st.session_state.get('sitting_1.0', 0),
    st.session_state.get('season_neg1', 0),
    st.session_state.get('season_neg033', 0),
    st.session_state.get('season_033', 0),
    st.session_state.get('season_10', 0),
    st.session_state.get('age_0.5', 0),
    st.session_state.get('age_1.0', 0)
]).reshape(1, -1)

# Display prediction results with button
st.write("---")  # Another divider line for clarity
if st.button(lang_dict["submit"]):
    predictions = model.predict(input_data)
    predicted_class = lang_dict["fertile"] if predictions[0][0] >= 0.5 else lang_dict["infertile"]
    predicted_probability = predictions[0][0] if predictions[0][0] >= 0.5 else 1 - predictions[0][0]
    
    st.success(f"{lang_dict['prediction']}: {predicted_class}")
    st.warning(lang_dict["consult_doctor"])


    # Provide recommendations based on input data
    recommendations = provide_recommendations(input_data)
    if recommendations:
        st.write(f"### {lang_dict['recommendations']}:")
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.write(lang_dict["no_recommendations"])

    # User feedback section
    st.write("---")
    user_feedback = st.text_area(lang_dict["feedback"])
    if st.button(lang_dict["submit_feedback"]):
        st.success(lang_dict["thank_you"])
