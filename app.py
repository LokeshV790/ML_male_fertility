import streamlit as st
import numpy as np
import tensorflow as tf
from utils.input_processing import update_inputs
from utils.recommendations import provide_recommendations
from utils.translations import translations  # Import translations

# Load your trained model
model = tf.keras.models.load_model('model/fertitlity_dn.h5')

# Language selection
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

# Now use lang_key to access translations
lang_dict = translations[lang_key]

# Streamlit app layout
st.title(translations[lang_key]["title"])
# st.image('assets/logo.png', width=300)  # Optional logo for branding

# User inputs
diseases = st.selectbox(translations[lang_key]["childhood_diseases"], ['Yes', 'No'])
accident = st.selectbox(translations[lang_key]["accident"], ['Yes', 'No'])
surgery = st.selectbox(translations[lang_key]["surgery"], ['Yes', 'No'])

fever = st.selectbox(translations[lang_key]["fever"], ['Fever < 3 Months (-1)', 'Fever > 3 Months (0)', 'No Fever (1)'], 
                      on_change=update_inputs, args=("fever", "fever"))
alcohol = st.selectbox(translations[lang_key]["alcohol"], ['Several Times a Day (0.2)', 'Every Day (0.4)', 
                                                      'Several Times a Week (0.6)', 'Once a Week (0.8)', 
                                                      'Hardly Ever (1.0)'], 
                       on_change=update_inputs, args=("alcohol", "alcohol"))
smoking = st.selectbox(translations[lang_key]["smoking"], ['Never (-1)', 'Occasionally (0)', 'Daily (1)'],
                       on_change=update_inputs, args=("smoking", "smoking"))
sitting = st.selectbox(translations[lang_key]["sitting"], ['0-8 hours', '9-16 hours'], 
                       on_change=update_inputs, args=("sitting", "sitting"))
season = st.selectbox(translations[lang_key]["season"], ['Winter (-1)', 'Spring (-0.33)', 'Summer (0.33)', 'Fall (1)'],
                       on_change=update_inputs, args=("season", "season"))
age = st.selectbox(translations[lang_key]["age"], ['27 Years or Under (0.5)', 'Over 27 Years (1.0)'],
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

# Predict and display results
if st.button(translations[lang_key]["submit"]):
    predictions = model.predict(input_data)
    predicted_class = translations[lang_key]["fertile"] if predictions[0][0] >= 0.5 else translations[lang_key]["infertile"]
    predicted_probability = predictions[0][0] if predictions[0][0] >= 0.5 else 1 - predictions[0][0]
    
    st.success(f"{translations[lang_key]['prediction']}: {predicted_class}")
    st.warning(translations[lang_key]["consult_doctor"])
    
    # Example static accuracy value
    accuracy = 0.85  # Replace with your actual model's accuracy if available
    st.write(f"{translations[lang_key]['model_accuracy']}: {accuracy * 100:.2f}%")

    # Get recommendations based on input data
    recommendations = provide_recommendations(input_data)
    
    if recommendations:
        st.write(f"### {translations[lang_key]['recommendations']}:")
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.write(translations[lang_key]["no_recommendations"])

    # User feedback section
    user_feedback = st.text_area(translations[lang_key]["feedback"])
    if st.button(translations[lang_key]["submit_feedback"]):
        st.success(translations[lang_key]["thank_you"])
