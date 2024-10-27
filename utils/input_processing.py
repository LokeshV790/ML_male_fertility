import streamlit as st

def update_inputs(selected, category):
    # Resetting all related inputs to 0 based on the category
    if category == 'season':
        st.session_state['season_neg1'] = 0
        st.session_state['season_neg033'] = 0
        st.session_state['season_033'] = 0
        st.session_state['season_10'] = 0
        
        if selected == 'Winter (-1)':
            st.session_state['season_neg1'] = 1
        elif selected == 'Spring (-0.33)':
            st.session_state['season_neg033'] = 1
        elif selected == 'Summer (0.33)':
            st.session_state['season_033'] = 1
        elif selected == 'Fall (1)':
            st.session_state['season_10'] = 1

    elif category == 'alcohol':
        st.session_state['alcohol_0.2'] = 0
        st.session_state['alcohol_0.4'] = 0
        st.session_state['alcohol_0.6'] = 0
        st.session_state['alcohol_0.8'] = 0
        st.session_state['alcohol_1.0'] = 0
        
        if selected == 'Several Times a Day (0.2)':
            st.session_state['alcohol_0.2'] = 1
        elif selected == 'Every Day (0.4)':
            st.session_state['alcohol_0.4'] = 1
        elif selected == 'Several Times a Week (0.6)':
            st.session_state['alcohol_0.6'] = 1
        elif selected == 'Once a Week (0.8)':
            st.session_state['alcohol_0.8'] = 1
        elif selected == 'Hardly Ever (1.0)':
            st.session_state['alcohol_1.0'] = 1

    elif category == 'smoking':
        st.session_state['smoking_-1'] = 0
        st.session_state['smoking_0'] = 0
        st.session_state['smoking_1'] = 0
        
        if selected == 'Never (-1)':
            st.session_state['smoking_-1'] = 1
        elif selected == 'Occasionally (0)':
            st.session_state['smoking_0'] = 1
        elif selected == 'Daily (1)':
            st.session_state['smoking_1'] = 1

    elif category == 'fever':
        st.session_state['fever_neg1'] = 0
        st.session_state['fever_0'] = 0
        st.session_state['fever_1'] = 0
        
        if selected == 'Fever < 3 Months (-1)':
            st.session_state['fever_neg1'] = 1
        elif selected == 'Fever > 3 Months (0)':
            st.session_state['fever_0'] = 1
        elif selected == 'No Fever (1)':
            st.session_state['fever_1'] = 1

    elif category == 'sitting':
        st.session_state['sitting_0.5'] = 0
        st.session_state['sitting_1.0'] = 0
        
        if selected == '0-8 hours':
            st.session_state['sitting_0.5'] = 1
        elif selected == '9-16 hours':
            st.session_state['sitting_1.0'] = 1

    elif category == 'age':
        st.session_state['age_0.5'] = 0
        st.session_state['age_1.0'] = 0
        
        if selected == '27 Years or Under (0.5)':
            st.session_state['age_0.5'] = 1
        elif selected == 'Over 27 Years (1.0)':
            st.session_state['age_1.0'] = 1
