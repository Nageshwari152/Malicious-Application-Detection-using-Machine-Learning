import time
import os
from PIL import Image
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# load user details from dotenv file
# userName = os.environ.get("USER")
# password = os.environ.get("PASSWORD")
userName = "Admin"
password = "123"


logStatus = False
title = st.empty()
if logStatus == False:
    title.markdown("<h1 style='text-align: center; color: #ffff;'>Admin Login</h1>",
                   unsafe_allow_html=True)

userContainer = st.empty()
passwordContainer = st.empty()
user = userContainer.text_input('Admin ID')
passCode = passwordContainer.text_input('Input Password', type="password")


# check log in credentials
if user != "" and passCode != "" and user == userName and passCode == password:
    title.empty()
    logStatus = True

elif user != "" and passCode != "" and (user != userName or passCode != password):
    st.warning('Wrong ID or Password! please try again')

if user == userName and passCode == password:
    userContainer.empty()
    passwordContainer.empty()
    time.sleep(1)

# while the log in credentials(logStatus) is TRUE
if logStatus:

    image = Image.open("dynamic-file-analysis.jpg")

    st.image(image, use_column_width=True)
    st.markdown("<h1 style='text-align: center; color: #ffff;'> Android Malware Detection</h1>",
                unsafe_allow_html=True)

    st.write("""
    #####  This detects whether the Application is Malicious or Benign

    
    """)

    st.sidebar.header('Input Android App Features')

    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader(
        "Upload your input CSV file", type=["csv"])

    if uploaded_file:

        data = pd.read_csv(uploaded_file)
        test = data.astype(str)
        st.dataframe(test)

        if st.button('Feature Selection'):
            # Performe Feature Extraction

            dataToUse = data[['SEND_SMS', 'android.telephony.SmsManager', 'READ_PHONE_STATE',
                              'RECEIVE_SMS', 'READ_SMS', 'android.intent.action.BOOT_COMPLETED',
                              'TelephonyManager.getLine1Number', 'WRITE_SMS',
                              'WRITE_HISTORY_BOOKMARKS', 'TelephonyManager.getSubscriberId',
                              'android.telephony.gsm.SmsManager', 'INSTALL_PACKAGES',
                              'READ_HISTORY_BOOKMARKS', 'INTERNET', 'AUTHENTICATE_ACCOUNTS',
                              'android.os.IBinder', 'IBinder', 'Binder', 'CAMERA',
                              'READ_SYNC_SETTINGS', 'Ljava.lang.Class.forName', 'Runtime.getRuntime',
                              'Ljava.lang.Object.getClass', 'mount', 'android.intent.action.SEND',
                              'USE_CREDENTIALS', 'MANAGE_ACCOUNTS', 'Ljavax.crypto.Cipher',
                              'System.loadLibrary', 'DexClassLoader', 'getCallingUid', 'SecretKey',
                              'Ljava.lang.Class.getMethod', 'HttpGet.init', 'KeySpec',
                              'android.content.pm.PackageInfo', 'Ljavax.crypto.spec.SecretKeySpec',
                              'getBinder', 'GET_ACCOUNTS', 'Ljava.lang.Class.getDeclaredField',
                              'Landroid.content.Context.unregisterReceiver',
                              'Ljava.lang.Class.getField',
                              'Landroid.content.Context.registerReceiver', 'ClassLoader',
                              'android.content.pm.Signature', 'Ljava.lang.Class.getMethods',
                              'Ljava.lang.Class.cast', 'Ljava.net.URLDecoder',
                              'Ljava.lang.Class.getCanonicalName', 'attachInterface',
                              'android.os.Binder', 'ServiceConnection', 'bindService',
                              'onServiceConnected', 'transact']]
            title2 = st.empty()
            title2.write("Selecting feature...")
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.05)
                my_bar.progress(percent_complete + 1)
            my_bar.empty()
            title2.empty()
            my_bar.success('Feature Selected Successfully!')
            time.sleep(2)
            my_bar.empty()

            # Reads in saved classification model
            dataModel = pickle.load(
                open('stacking.pki', 'rb'))

            # Apply model to make predictions
            prediction = dataModel.predict(dataToUse)
            prediction_proba = dataModel.predict_proba(dataToUse)

            modelDetection = np.array(['Benign', 'Malicious'])
            # st.write(modelDetection[prediction])

            st.subheader('Prediction Probability')
            st.write(prediction_proba)

            if (modelDetection[prediction][0] == "Benign"):
                st.write("### STATUS: 'BENIGN' ", )
            else:
                st.write("### STATUS: 'MALWARE' ", )
        else:
            st.write('Click 👆 To Perform Feature selection')
    else:
        st.write("Waiting for CSV file to be uploaded...")
