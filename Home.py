import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(
     page_title="VisTool",
     page_icon=":bar_chart:",
     initial_sidebar_state="auto"
 )
st.title("About This Project...")
"""
Anonymization is a crucial technique for safeguarding individual privacy, preventing data misuse,
 or identification of specific individuals. It helps mitigate potential privacy risks, 
 making data more secure and compliant with data privacy regulations. 
 
In the context of anonymized data, there exists a trade-off between information loss and privacy protection.
Anonymization typically involves removing or blurring individual identity information to ensure that
 data is no longer associated with specific individuals. This means that some details and specific associations in the original data may be lost,
  reducing the accuracy and granularity of the data.
  
When anonymizing data, a balance needs to be struck between information loss and privacy protection.
 Stronger anonymization may result in greater information loss, while weaker anonymization might not provide sufficient privacy protection.
  Finding the right balance is essential to meet the requirements of data privacy regulations while maintaining the utility of the data.

__In this project, we provide users a tool to help finding the right trade-off between utility and privacy.__  
In order to help us improve the usability of the tool, we set  three test iterations. In __exploration,__ we apply
 various components to prove which one has positive affects on finding optimal trade-offs. In __improvement__ we focus on
  user interactions and let the users test a high fidelity prototype. In __Validation,__ we validate if the UI problems appears in 
  the second iteration have been solved or not.
"""
lottie_loading_url = "https://assets6.lottiefiles.com/packages/lf20_ic37y4kv.json"
lottie_loading = load_lottieurl(lottie_loading_url)

st_lottie(lottie_loading,key="loading")

hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
	content:'Master project of Zheng Yao'; 
    visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)