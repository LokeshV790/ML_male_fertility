import streamlit as st
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model('model/fertitlity_dn.h5')

# Function to reset related inputs based on selections
def update_inputs(selected, category):
    if category == 'season':
        st.session_state['season_neg1'] = 1 if selected == 'Winter (-1)' else 0
        st.session_state['season_neg033'] = 1 if selected == 'Spring (-0.33)' else 0
        st.session_state['season_033'] = 1 if selected == 'Summer (0.33)' else 0
        st.session_state['season_10'] = 1 if selected == 'Fall (1)' else 0

    elif category == 'fever':
        st.session_state['fever_neg1'] = 1 if selected == 'Fever < 3 Months (-1)' else 0
        st.session_state['fever_0'] = 1 if selected == 'Fever > 3 Months (0)' else 0
        st.session_state['fever_1'] = 1 if selected == 'No Fever (1)' else 0

    elif category == 'alcohol':
        options = ['Several Times a Day (0.2)', 'Every Day (0.4)', 'Several Times a Week (0.6)', 
                   'Once a Week (0.8)', 'Hardly Ever (1.0)']
        for i, option in enumerate(options):
            st.session_state[f'alcohol_{0.2 + i * 0.2}'] = 1 if option == selected else 0

    elif category == 'smoking':
        options = ['Never (-1)', 'Occasionally (0)', 'Daily (1)']
        for i, option in enumerate(options):
            st.session_state[f'smoking_{-1 + i}'] = 1 if option == selected else 0

    elif category == 'sitting':
        st.session_state['sitting_0.5'] = 1 if selected == '0-8 hours' else 0
        st.session_state['sitting_1.0'] = 1 if selected == '9-16 hours' else 0

    elif category == 'age':
        st.session_state['age_0.5'] = 1 if selected == '27 Years or Under (0.5)' else 0
        st.session_state['age_1.0'] = 1 if selected == 'Over 27 Years (1.0)' else 0

# Streamlit app layout
st.title("Male Fertility Prediction")

# User inputs
diseases = st.selectbox("Childhood Diseases (Yes/No)", ['Yes', 'No'])
accident = st.selectbox("Accident or Trauma (Yes/No)", ['Yes', 'No'])
surgery = st.selectbox("Surgery (Yes/No)", ['Yes', 'No'])

fever = st.selectbox("Select Fever", 
    ['Fever < 3 Months (-1)', 'Fever > 3 Months (0)', 'No Fever (1)'], 
    on_change=update_inputs, args=("fever", "fever"))

alcohol = st.selectbox("Select Alcohol Consumption", 
    ['Several Times a Day (0.2)', 'Every Day (0.4)', 'Several Times a Week (0.6)', 
     'Once a Week (0.8)', 'Hardly Ever (1.0)'], 
    on_change=update_inputs, args=("alcohol", "alcohol"))

smoking = st.selectbox("Select Smoking Frequency", 
    ['Never (-1)', 'Occasionally (0)', 'Daily (1)'], 
    on_change=update_inputs, args=("smoking", "smoking"))

sitting = st.selectbox("Select Sitting Hours", 
    ['0-8 hours', '9-16 hours'], 
    on_change=update_inputs, args=("sitting", "sitting"))

season = st.selectbox("Select Season", 
    ['Winter (-1)', 'Spring (-0.33)', 'Summer (0.33)', 'Fall (1)'], 
    on_change=update_inputs, args=("season", "season"))

age = st.selectbox("Select Age Group", 
    ['27 Years or Under (0.5)', 'Over 27 Years (1.0)'], 
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
    predicted_class = "Fertile" if predictions[0][0] < 0.5 else "Infertile"
    predicted_probability = predictions[0][0] if predictions[0][0] >= 0.5 else 1 - predictions[0][0]

    st.success(f"Prediction: {predicted_class}")
    st.write(f"Probability of being Fertile: {predicted_probability:.2f}")

    # Example static accuracy value
    accuracy = 0.85
    st.write(f"Model Accuracy: {accuracy * 100:.2f}%")
