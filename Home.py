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
language = st.radio('Language',['🇬🇧','🇨🇳'],captions=['EN','中文'],horizontal=True)
if language =='🇬🇧':
    with st.container():
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
elif language =='🇨🇳':
    with st.container():
        st.title("关于这个项目...")
        """
        匿名化是保护个人隐私、防止数据滥用的关键技术。它有助于降低潜在的隐私风险，使数据更加安全并符合数据隐私法规。
        但是在进行数据匿名化时，信息丢失和隐私保护之间存在权衡。匿名化通常涉及删除或模糊个人身份信息，以确保
         数据不再与特定个人相关。这意味着原始数据中的一些细节和特定关联可能会丢失，从而降低数据的准确性。
          
        数据匿名化时，需要在信息丢失和隐私保护之间取得平衡。较强的匿名化可能会导致更大的信息丢失，
        而较弱的匿名化可能无法提供足够的隐私保护，所以找到适当的平衡点至关重要。
        
        __在这个项目中，我们为用户提供了一个工具来帮助他们在实用性和隐私之间找到正确的权衡。__
        为了帮助我们提高工具的可用性，我们设置了三个测试迭代。在__Exploration__中，我们应用
         各种组件来测试哪一个对找到最佳权衡具有积极影响。在__Improvement__中，我们专注于用户交互并让用户测试高保真原型。在 __Validation,__ 中，我们验证第二次迭代中的UI问题是否已解决。
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