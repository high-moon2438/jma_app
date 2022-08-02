import streamlit as st
import pandas as pd
import base64
import numpy as np

st.title("データ変換アプリ")
st.caption('日データを月別・年別に変換します。')

with st.form(key='resample_form'):

    upfile = st.file_uploader("ファイルアップロード",type ='csv')
    submit_btn = st.form_submit_button('データ取得')
    if submit_btn:                      #取得開始処理
        st.text("データ取得中") 
        dfinput = pd.read_csv(upfile, index_col='day', parse_dates=True)
        df = dfinput.replace('-9999.0','#N/A')
        swich = 0 #今年のデータ含まれるかどうかの判定


        #時間別データを単位別に出力する
        df_SUM_Y  = df.resample('Y').sum()
        df_MEAN_Y = df.resample('Y').mean()
        df_SUM_M  = df.resample('M').sum()
        df_MEAN_M = df.resample('M').mean()
        df_SUM_D  = df.resample('D').sum()
        
        csv01 = df_SUM_Y.to_csv()
        b64_01 = base64.b64encode(csv01.encode()).decode()
        href_01 = f'<a href="data:application/octet-stream;base64,{b64_01}" download="01_SUM_Y.csv">download_link</a>'  
        st.markdown(f"年合計データ => {href_01}",unsafe_allow_html=True)  
        
        csv02 = df_MEAN_Y.to_csv()
        b64_02 = base64.b64encode(csv02.encode()).decode()
        href_02 = f'<a href="data:application/octet-stream;base64,{b64_02}" download="02_MEAN_Y.csv">download_link</a>'  
        st.markdown(f"年平均データ => {href_02}",unsafe_allow_html=True)
        
        csv03 = df_SUM_M.to_csv()
        b64_03 = base64.b64encode(csv03.encode()).decode()
        href_03 = f'<a href="data:application/octet-stream;base64,{b64_03}" download="03_SUM_M.csv">download_link</a>'  
        st.markdown(f"月合計データ => {href_03}",unsafe_allow_html=True) 
        
        csv04 = df_MEAN_Y.to_csv()
        b64_04 = base64.b64encode(csv04.encode()).decode()
        href_04 = f'<a href="data:application/octet-stream;base64,{b64_04}" download="04_MEAN_M.csv">download_link</a>'  
        st.markdown(f"月平均データ => {href_04}",unsafe_allow_html=True)  
        


                        
                
                
                