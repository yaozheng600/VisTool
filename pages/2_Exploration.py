import json
import tempfile
from google.cloud import storage
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import altair as alt
import math
import Interface_config as ic
from Anony.preserver import Preserver
from Measurement import Measurement

with open(st.secrets["GOOGLE_CLOUD_CREDENTIALS_JSON"], "r") as file:
    credential_path = json.load(file)
client = storage.Client.from_service_account_json(credential_path)
bucket_name = "survey_masterarbeit"
csv_file_name = "survey_1_iteration"
survey = pd.DataFrame(data=[3],columns=['Age'])
privacy_policy = open("privacy_policy.txt")

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
def pre_questionnaire():
    with st.container():
            survey['Age']=st.number_input(label="__Q1: Your Age__",min_value=1,max_value=100,value=18)
            survey['Gender']=st.radio(label="__Q1: Your gender__",options=["Male", "Female", "others"], horizontal=True)
            survey['EL']=st.radio(label="__Q2: Your education level__", options=["Less than a high school diploma", 'High school graduate or equivalent',
                                            'Bachelor degree or higher'])
            survey['Data_exp']=st.radio(label="__Q3: Your experience in working with data__",
                                     options=["Data newbie","Data beginner","Data expert"])
def SEQ(task_num):
    with st.container():
        st.write("__Question: How do you expect the ease of this task?__")
        col1, col2, col3 = st.columns([3, 7, 2])
        with col1:
            st.write("very difficult")
        with col2:
            survey[f'SEQ task{task_num}']=st.radio(options=[1, 2, 3, 4, 5, 6, 7], horizontal=True, label_visibility="collapsed",
                                             label=f"SEQ_task{task_num}")
        with col3:
            st.write("very easy")
def ASQ(task_num):
    with st.container():
        st.write("You finished this task, please grade this task according to your user experience:")
        """
        __1. Overall, I am satisfied with the ease of completing the task in this scenario.__
        """
        col_1, col_2, col_3 = st.columns([3, 7, 2])
        with col_1:
            st.write("strongly disagree")
        with col_2:
            survey[f'ASQ task{task_num}_1'] = st.radio(options=[1, 2, 3, 4, 5, 6, 7],horizontal=True,
                                                         label_visibility="collapsed",
                                                         label=f"ASQ_task{task_num}_1")
        with col_3:
            st.write("strongly agree")
        """
        __2. Overall, I am satisfied with the amount of time it took to complete the task in this scenario.__
        """
        col_1, col_2, col_3 = st.columns([3, 7, 2])
        with col_1:
            st.write("strongly disagree")
        with col_2:
            survey[f'ASQ task{task_num}_2'] = st.radio(options=[1, 2, 3, 4, 5, 6, 7], horizontal=True,
                                                     label_visibility="collapsed",
                                                     label=f"ASQ_task{task_num}_2")
        with col_3:
            st.write("strongly agree")
        """
        __3. Overall, I am satisfied with the support information (tips, user interaction) when completing the task.__
        """
        col_1, col_2, col_3 = st.columns([3, 7, 2])
        with col_1:
            st.write("strongly disagree")
        with col_2:
            survey[f'ASQ task{task_num}_3'] = st.radio(options=[1, 2, 3, 4, 5, 6, 7], horizontal=True,
                                                     label_visibility="collapsed",
                                                     label=f"ASQ_task{task_num}_3")
        with col_3:
            st.write("strongly agree")
def confidence_Q(task_num):
    st.write(
        "Are you sure that you have done a good decision to balance the utility and privacy for anonymizaed data?")
    col1, col2, col3 = st.columns([3, 7, 2])
    with col1:
        st.write("I'm very not sure")
    with col2:
        survey[f'Confidence_{task_num}'] = st.radio(options=[1, 2, 3, 4, 5, 6, 7], horizontal=True,
                                                 label_visibility="collapsed",
                                                 label=f'Confidence_{task_num}')
    with col3:
        st.write("I'm very sure")
def select_attributes(data):
    QIs = st.multiselect(label="__Select attributes you want to publish:__",options=data.columns)
    SA = st.selectbox(label="__Select a sensitive attribute:__",options=data.columns.drop(QIs))
    return QIs,SA
def spreadsheet(data):
    with st.spinner(text="In progress..."):
        tab2, tab1, tab3 = st.tabs(["🗃 Data", "📉 Description", "📈 Detail in Chart"])
        with tab1:
            st.subheader("Numeric Atrributes")
            st.write(data.describe())
            st.subheader("Categorical Atrributes")
            st.write(ic.df_describe(data.describe(exclude=[np.number])))
        with tab2:
            st.subheader("Original Data")
            st.write(data)
        with tab3:
            st.subheader("Chart")
            options = st.multiselect("Select the atrributes you want to see in detail",
                                     options=data.columns,
                                     default=data.columns[1])
            for i, df in enumerate(options):
                st.altair_chart(ic.barchart_describe(data[df]))
def indicater(measurement,measurement_pre):
    with st.spinner("In progress..."):
        utility_loss = measurement.utility_loss()
        privacy_loss = max(measurement.privacy_loss())
        col_1,col_2 =st.columns([1,1])
        col_1.metric(label="Utility Loss", help="from 0(no loss) to 1(serious loss)",
                     value=utility_loss,delta=utility_loss-measurement_pre[0],delta_color='inverse')
        col_2.metric(label="Privacy Loss", help="from 0(no loss) to 1(serious loss)",
                     value=privacy_loss,delta=privacy_loss-measurement_pre[1],delta_color='inverse')
    st.session_state["measure_pre"] = [utility_loss, privacy_loss]
def select_anony_method(data,task,QIs,SA,pcc=False):
    parameters =[]
    st.write("__Use the following tool to achieve this goal.__")
    col_1,col_2 = st.columns([1,2])
    with col_1:
        st.write("__Anonymization method__")
        method = st.radio(label_visibility='collapsed',label="__Seclect an anonymization method:__",options=['k-anonymity','l-diversity','t-closeness'],key=task,help="Each method considers the privacy protecting from different perspectives.")
    with col_2:
        st.write("__Parameters__")
        if pcc:
            p = st.slider(label="__p__ value:",min_value=0.0,max_value=1.0,step=0.01,key=f"p_{task}",help="0 is lowest privacy level and 1 is highest.")
            parameters = PCC(p,data[SA].nunique())
            return anonymization(data, QIs, SA, method, parameters)
        col2_1,col2_2 = st.columns([1,1])
        with col2_1:
            k = st.slider(label="__k__ value:",min_value=1,max_value=10,value=5,key=f"k_{task}",help="This parameter is needed in all of the given 3 methods. In general, a high value indicates high privacy but leads to more information loss.")
            parameters.append(k)
        with col2_2:
            if method=="l-diversity":
                l = st.slider(label="__l__ value:",min_value=1,max_value=data[SA].nunique(),key=f"l_{task}",help="This parameter is needed in l-diversity. In general, a high value indicates high privacy but leads to more information loss.")
                parameters.append(l)
            elif method=="t-closeness":
                t = st.slider(label="__t__ value:", min_value=0.0, max_value=1.0,value=0.25,step=0.01,key=f"t_{task}",
                              help="This parameter is needed in t-closeness. In general, a high value indicates high privacy but leads to more information loss.")
                parameters.extend([1,t])

    return anonymization(data,QIs,SA,method,parameters)
@st.cache_data
def PCC(p,num_sa,k_max=10):
    l_max = num_sa
    t_min = 1/l_max

    k = max(1,math.ceil(p*k_max))
    l = max(1,math.ceil(math.log2(k)))
    t = max(t_min,(l_max*t_min)/(1+l*p))

    return [k,l,t,p]
def effectiveness(data,anony_data,QIs,SA):
    measure = Measurement(data, anony_data, QIs, SA)
    utility_loss = measure.utility_loss()
    privacy_loss = max(measure.privacy_loss())
    E = pow((utility_loss*privacy_loss+pow(utility_loss-privacy_loss,2)),-1)
    return E
def anonymization(data,QIs,SA,method,parameters):
    def check_dtype(df):
        for col in df.columns:
            if df[col].dtype.name == 'object':
                df[col] = df[col].astype('category')
    check_dtype(data)
    anony = Preserver(data,QIs,SA)
    if method=="k-anonymity":
        return pd.DataFrame(anony.k_anonymity(parameters[0]))
    elif method=="l-diversity":
        return pd.DataFrame(anony.l_diversity(k=parameters[0],l=parameters[1]))
    elif method=="t-closeness":
        return pd.DataFrame(anony.t_closeness(k=parameters[0],t=parameters[2]))
def Auto_PCC(data,QIs,SA,loop_num=101,k_max=10):
    num_SA = data[SA].nunique()
    parameters = []
    p = []
    P_loss = []
    U_loss = []
    method = []
    k = []
    l = []
    t = []

    for i in range(loop_num):
        p_value = i / (loop_num-1)
        parameters.append(PCC(p_value,num_SA,k_max))

    progress_text = "Operation in progress. Please wait."
    progress_bar = st.progress(0.0, text=progress_text)
    for i in range(loop_num):
        df_k = anonymization(data, QIs, SA, method='k-anonymity', parameters=parameters[i])
        df_l = anonymization(data, QIs, SA, method='l-diversity', parameters=parameters[i])
        df_t = anonymization(data, QIs, SA, method='t-closeness', parameters=parameters[i])

        measure_k = Measurement(data, df_k, QIs, SA)
        measure_l = Measurement(data, df_l, QIs, SA)
        measure_t = Measurement(data, df_t, QIs, SA)

        P_loss.append(max(measure_k.privacy_loss()))
        P_loss.append(max(measure_l.privacy_loss()))
        P_loss.append(max(measure_t.privacy_loss()))

        U_loss.append(measure_k.utility_loss())
        U_loss.append(measure_l.utility_loss())
        U_loss.append(measure_t.utility_loss())

        method.extend(['K-anonymity', 'L-diversity', 'T-closeness'])
        k.extend([parameters[i][0], parameters[i][0], parameters[i][0]])
        l.extend([' ', parameters[i][1], ' '])
        t.extend(['', '', parameters[i][2]])
        p.extend([parameters[i][3], parameters[i][3], parameters[i][3]])
        progress_bar.progress(p[i], text=progress_text)

    progress_bar.empty()
    info = pd.DataFrame(
        {
            'p': p,
            "P_loss": P_loss,
            "U_loss": U_loss,
            "method": method,
            'k': k,
            'l': l,
            't': t
        }
    )
    return info
def visualization(info):
    selector = alt.selection_point()
    base = alt.Chart(info).properties(
        title="Utility Privacy trade-off"
    ).add_params(selector)

    point = base.mark_point(filled=True).encode(
        x=alt.X("P_loss", title="P_loss"),
        y=alt.Y("U_loss", title="U_loss"),
        tooltip=['p', "U_loss", 'P_loss', 'method', 'k', 'l:N', 't'],
        opacity=alt.OpacityValue(0.5),
        color=alt.condition(selector, 'method', alt.value('lightgray')),
    )
    st.altair_chart(point,use_container_width=True)

st.title("Exploration")
"""
Welcome to join the Test! 

Now, please take it easy. All you need to do is following the steps below and complete the given tasks.
Soooo, let's start!
"""
st.header("Step 0: Some preparation")
st.markdown("Please read our privacy policy.")
with st.expander("Privacy policy..."):
    st.markdown(privacy_policy.read())
    privacy_aggree=st.toggle("I agree")

if privacy_aggree:
    st.subheader("Let us know more about you")
    pre_questionnaire()
    st.divider()
    st.subheader("A file you need for the test")
    st.write("Please click this link to download our test data file. File name: Test.csv. You may use your own dataset.")

    data = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    csv = convert_df(data)
    if st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="text.csv"
        ):
        st.success("You have downloaded the file successfully!")
    st.divider()

    st.header("Task 1: upload a data set")
    """
    You have some data and wanna publish it. Due to privacy-protecting consideration,
    you use our VisTool to anonymize the data. First, you should upload your data for further process.
    """
    SEQ(task_num=1)
    st.markdown("Use the following UI component to upload a CSV file.")
    uploaded_data = st.file_uploader("Upload your CSV file here",type="CSV")
    if uploaded_data:
        data = pd.read_csv(uploaded_data)
        data = data.drop(data.columns[0],axis=1)
        ASQ(task_num=1)
        st.divider()
        with st.container():
            st.header("Task2 : Select the attributes you are interested in")
            """
            You need to select some attributes of the data that you wanna show to the public.
             Among these attributes, there is a __sensitive attribute__ which is a "secret" of an individual.
             The anonymization process will protect it by masking other attibutes. Your task in this step is:
             
             1. Select some attributes of the data that you want to publish.
             2. Select a sensitive attribute.
            """
            SEQ(task_num=2)
            st.write("__Use the following tool to achieve this goal.__")
            spreadsheet(data)
            QIs,SA = select_attributes(data)
            if QIs and SA:
                ASQ(task_num=2)
        st.divider()
        with st.container():
            st.header("Task 3: Select your anonymization parameters-1")
            """
            Now, you need to select a method for anonymization. We provide [k-anonymity](https://en.wikipedia.org/wiki/K-anonymity), [l-diversity](https://en.wikipedia.org/wiki/L-diversity), 
            and [t-closeness](https://en.wikipedia.org/wiki/T-closeness). In order to get a good anonymization result,
             you need to modify the parameters of the method. Check the anonymized data in the spreadsheet.
            """
            SEQ(task_num=3)
            anony_data_3 = select_anony_method(data,task=3,QIs=QIs,SA=SA)
            confirm_3 = st.toggle("Confirm your choice",key="task_3")
            if confirm_3:
                survey[f"Effectiveness_Task{3}"] = effectiveness(data,anony_data_3,QIs,SA)
            if isinstance(anony_data_3,pd.DataFrame):
                spreadsheet(anony_data_3)
            if confirm_3:
                confidence_Q(task_num=3)
                ASQ(task_num=3)
        st.divider()
        with st.container():
            st.header("Task 4: Select your anonymization parameters-2")
            """
            We provide you here an indicator of the utility- and privacy-loss. With the help
            of this indicator, maybe you have a new idea to modify your anonymization parameters?
            If so, please re-modify the anonymization method and parameters. You can also insist your choise from last task. 
            """
            SEQ(task_num=4)
            if "measure_pre" not in st.session_state:
                st.session_state["measure_pre"]=[0,0]
            anony_data_4 = select_anony_method(data, task=4,QIs=QIs, SA=SA)
            if isinstance(anony_data_4,pd.DataFrame):
                measure = Measurement(data,anony_data_4,QIs,SA)
                measure_pre=indicater(measure,st.session_state["measure_pre"])
            if st.toggle("Confirm your choice",key="task_4"):
                survey[f"Effectiveness_Task{4}"] = effectiveness(data, anony_data_4, QIs, SA)
                confidence_Q(task_num=4)
                ASQ(task_num=4)
        st.divider()
        with st.container():
            st.header("Task 5: Select your anonymization parameters-3")
            """
            In this task, we integrate the parameter k, l, and t in one parameter p,
             which present low privacy to high privacy from 0 to 1. Modify parameter p to get 
             an optimal balance of privacy and utility you think.
            """
            SEQ(task_num=5)
            if "measure_pre" not in st.session_state:
                st.session_state["measure_pre"]=[0,0]
            anony_data_5 = select_anony_method(data, task=5,QIs=QIs, SA=SA,pcc=True)
            if isinstance(anony_data_5,pd.DataFrame):
                measure = Measurement(data,anony_data_5,QIs,SA)
                measure_pre=indicater(measure,st.session_state["measure_pre"])
            if st.toggle("Confirm your choice",key="task_5"):
                survey[f"Effectiveness_Task{5}"] = effectiveness(data, anony_data_5, QIs, SA)
                confidence_Q(task_num=5)
                ASQ(task_num=5)
        st.divider()
        with st.container():
            st.header("Task 6: Select your anonymization parameters-4")
            """
            In this task, we run the parameter p from 0 to 1 automatically.
             Following visualization shows utility loss and privacy loss
             in one scatter plot. With the help of this scatter plot, please 
             select an optimal balance of privacy and utility you think.
            """
            SEQ(task_num=6)
            if st.button("Run the anonymization progress",type="primary"):
                info = Auto_PCC(data,QIs,SA,loop_num=11)
                visualization(info)
            anony_data_6 = select_anony_method(data, task=6, QIs=QIs, SA=SA, pcc=True)
            if st.toggle("Confirm your choice",key="task_6"):
                survey[f"Effectiveness_Task{6}"] = effectiveness(data, anony_data_6, QIs, SA)
                confidence_Q(task_num=6)
                ASQ(task_num=6)
                submit =st.button("Submit my questionnaire",type='primary',key="submit_survey",disabled=st.session_state.submit_survey)
                if submit:

                    bucket = client.get_bucket(bucket_name)
                    blob = bucket.blob(csv_file_name)
                    if blob.exists():
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv_file:
                            blob.download_to_filename(temp_csv_file.name)
                            # 转化云存储上的CSV文件为DataFrame
                            cloud_data = pd.read_csv(temp_csv_file.name)
                        merged_data = pd.concat([cloud_data,survey],ignore_index=True)
                    else:
                        merged_data = survey
                    merged_csv = merged_data.to_csv(index=False)
                    blob.upload_from_string(merged_csv,content_type='csv')
                    st.success("Your questionnaire is submitted, you may leave this web page.")
                    lottie_code = load_lottiefile('style/thank_you.json')
                    st_lottie(lottie_code,height=500,width=500, key="thank you")
        st.divider()
# data_json = survey.to_json(orient='records',date_format='iso')
# st.dataframe(json.loads(data_json))
# st.dataframe(survey)

hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
	content:'Master project of Zheng Yao.'; 
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
