import streamlit as st
import numpy as np
import tensorflow as tf
from utils.input_processing import update_inputs
from utils.recommendations import provide_recommendations

# Load your trained model
model = tf.keras.models.load_model('model/fertitlity_dn.h5')

# Streamlit app layout
st.title("Male Fertility Prediction")
# st.image('assets/logo.png', width=300)  # Optional logo for branding

# User inputs
diseases = st.selectbox("Childhood Diseases (Yes/No)", ['Yes', 'No'])
accident = st.selectbox("Accident or Trauma (Yes/No)", ['Yes', 'No'])
surgery = st.selectbox("Surgery (Yes/No)", ['Yes', 'No'])

fever = st.selectbox("Select Fever", ['Fever < 3 Months (-1)', 'Fever > 3 Months (0)', 'No Fever (1)'], 
                      on_change=update_inputs, args=("fever", "fever"))
alcohol = st.selectbox("Select Alcohol Consumption", ['Several Times a Day (0.2)', 'Every Day (0.4)', 
                                                      'Several Times a Week (0.6)', 'Once a Week (0.8)', 
                                                      'Hardly Ever (1.0)'], 
                       on_change=update_inputs, args=("alcohol", "alcohol"))
smoking = st.selectbox("Select Smoking Frequency", ['Never (-1)', 'Occasionally (0)', 'Daily (1)'],
                       on_change=update_inputs, args=("smoking", "smoking"))
sitting = st.selectbox("Select Sitting Hours", ['0-8 hours', '9-16 hours'], 
                       on_change=update_inputs, args=("sitting", "sitting"))
season = st.selectbox("Select Season", ['Winter (-1)', 'Spring (-0.33)', 'Summer (0.33)', 'Fall (1)'],
                       on_change=update_inputs, args=("season", "season"))
age = st.selectbox("Select Age Group", ['27 Years or Under (0.5)', 'Over 27 Years (1.0)'],
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
if st.button("Predict Fertility"):
    predictions = model.predict(input_data)
    predicted_class = "Fertile" if predictions[0][0] >= 0.5 else "Infertile"
    predicted_probability = predictions[0][0] if predictions[0][0] >= 0.5 else 1 - predictions[0][0]
    
    st.success(f"Prediction: {predicted_class}")
    # st.write(f"Probability of being Fertile: {predicted_probability:.2f}")
    st.warning(f"Consider consulting to your doctor, results may not be accurate")
    
    # Example static accuracy value
    accuracy = 0.85  # Replace with your actual model's accuracy if available
    st.write(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Get recommendations based on input data
    recommendations = provide_recommendations(input_data)
    
    if recommendations:
        st.write("### Recommendations:")
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.write("No specific recommendations based on your inputs.")

    # # User feedback section
    # user_feedback = st.text_area("Share your experience or feedback:")
    # if st.button("Submit Feedback"):
    #     st.success("Thank you for your feedback!")

