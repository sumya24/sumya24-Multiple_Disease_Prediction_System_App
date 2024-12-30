import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime

# Loading the saved models
diabetes_model = pickle.load(open('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/Pickle Model/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/Pickle Model/heart_model.sav', 'rb'))

# Paths to the CSV files for each disease
diabetes_csv_path = r'C:\Users\sumit\Desktop\Multiple Disease B.tech Project\diabetes_data.csv'
heart_csv_path = r'C:\Users\sumit\Desktop\Multiple Disease B.tech Project\heart_data.csv'


# Function to save data to CSV
def save_data_to_csv(data, file_path):
    try:
        df = pd.read_csv(file_path)
        new_row = pd.DataFrame([data])  # Create a DataFrame for the new row
        df = pd.concat([df, new_row], ignore_index=True)  # Concatenate the existing and new data
        df.to_csv(file_path, index=False)  # Save back to the CSV file
    except FileNotFoundError:
        new_row = pd.DataFrame([data])  # Create a DataFrame for the new row
        new_row.to_csv(file_path, index=False)  # Save to a new CSV file

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Information',
                            'Diabetes Prediction',
                            'Heart Disease Prediction'],
                           menu_icon='hospital',
                           icons=['info-circle','activity', 'heart-pulse', 'person'],
                           default_index=0)
# Information Page
if selected == 'Information':
    st.title('General Information')
    st.write("""
        
Machine learning has made significant strides in healthcare, 
particularly in early detection and management of chronic diseases like diabetes, 
heart disease, and hypertension, which are major contributors to global morbidity and mortality. 
Many people lack access to regular screenings, leading to late diagnoses and more complex treatments. 

This project, "Multiple Disease Prediction System using Machine Learning and Streamlit," aims to address this gap by providing a platform where users can input health data to receive predictions on their risk for diseases such as diabetes, heart disease, and Parkinson’s. Using machine learning algorithms and Streamlit for a user-friendly web interface, the app enables real-time predictions, 
democratizing early detection and improving global healthcare accessibility and efficiency.
    """)
    st.image('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/1st image.jpg', 
             caption='Stay Healthy, Stay Informed', 
             use_container_width=True)

    st.header("What is Diabetes?")
    st.write("""
        **Diabetes** is a chronic disease that occurs either when the pancreas does not produce enough insulin or when the body cannot effectively use the insulin it produces. 
        Insulin is a hormone that regulates blood glucose. Hyperglycaemia, also called raised blood glucose or raised blood sugar, 
        is a common effect of uncontrolled diabetes and over time leads to serious damage to many of the body's systems, 
        especially the nerves and blood vessels. 
        
        Common symptoms include: 
        
        - Frequent urination.
        - Increased thirst.
        - Unexplained weight loss.
        - Extreme fatigue.
        - Blurred vision.
    """)

    st.image('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/2nd image.png', 
             caption='Understanding Diabetes', 
             use_container_width=True)

    st.header("What is Heart Disease?")
    st.write("""
        **Heart Disease** is a common heart condition that affects the major blood vessels that supply the heart muscle. 
        A buildup of fats, cholesterol and other substances in and on the artery walls usually causes coronary artery disease. . 
        
        Common symptoms include:
        
        - Chest pain or discomfort.
        - Shortness of breath.
        - Pain, numbness, or weakness in your arms or legs.
        - Cold sweats, dizziness, or fatigue.
    """)

    st.image('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/3rd image.jpg', 
             caption='Understanding Heart Disease', 
             use_container_width=True)

    st.subheader("Health Tips")
    st.write("""
        Here are some general tips to maintain a healthy lifestyle and reduce the risk of chronic diseases:
        - Eat a balanced diet rich in vegetables, fruits, and whole grains.
        - Stay physically active—aim for at least 30 minutes of moderate exercise daily.
        - Avoid smoking and limit alcohol consumption.
        - Manage stress through relaxation techniques like meditation or yoga.
        - Regularly monitor your health and consult a doctor if necessary.
    """)

    st.image('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/4th image.jpeg', 
             caption='Understanding Health Tip', 
             use_container_width=True)


# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')
    
    st.image('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/diabetes 1.jpg', caption='Diabetes', use_container_width=True)

    # Getting the patient name
    patient_name = st.text_input('Patient Name')

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    # Code for Prediction
    diab_diagnosis = ''

    if st.button('Diabetes Test Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]
        try:
            user_input = [float(x) for x in user_input]
            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'

            # Save data to CSV
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            date, time = timestamp.split(' ')
            data = {
                'Patient Name': patient_name,
                'Pregnancies': Pregnancies,
                'Glucose': Glucose,
                'BloodPressure': BloodPressure,
                'SkinThickness': SkinThickness,
                'Insulin': Insulin,
                'BMI': BMI,
                'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
                'Age': Age,
                'Result': diab_diagnosis,
                'Date': date,
                'Time': time
            }
            save_data_to_csv(data, diabetes_csv_path)

            st.success(diab_diagnosis)

        except ValueError:
            st.error("Invalid input. Please make sure all values are numbers.")

    # Display the saved diabetes data
    st.subheader("Diabetes Data History")
    try:
        diabetes_df = pd.read_csv(diabetes_csv_path)
        st.dataframe(diabetes_df)
    except FileNotFoundError:
        st.warning("No diabetes data found.")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')
    
    st.image('C:/Users/sumit/Desktop/Multiple Disease B.tech Project/heart 1.jpeg', caption='Heart', use_container_width=True)

    # Getting the patient name
    patient_name = st.text_input('Patient Name')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # Code for Prediction
    heart_diagnosis = ''

    if st.button('Heart Disease Test Result'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        try:
            user_input = [float(x) for x in user_input]
            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'

            # Save data to CSV
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            date, time = timestamp.split(' ')
            data = {
                'Patient Name': patient_name,
                'Age': age,
                'Sex': sex,
                'Chest Pain Type': cp,
                'Resting Blood Pressure': trestbps,
                'Serum Cholesterol': chol,
                'Fasting Blood Sugar': fbs,
                'Resting ECG': restecg,
                'Max Heart Rate': thalach,
                'Exercise Induced Angina': exang,
                'Oldpeak': oldpeak,
                'Slope': slope,
                'CA': ca,
                'Thal': thal,
                'Result': heart_diagnosis,
                'Date': date,
                'Time': time
            }
            save_data_to_csv(data, heart_csv_path)

            st.success(heart_diagnosis)

        except ValueError:
            st.error("Invalid input. Please make sure all values are numbers.")

    # Display the saved heart disease data
    st.subheader("Heart Disease Data History")
    try:
        heart_df = pd.read_csv(heart_csv_path)
        st.dataframe(heart_df)
    except FileNotFoundError:
        st.warning("No heart disease data found.")
