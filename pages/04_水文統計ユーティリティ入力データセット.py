from random import randint
import streamlit as st
import pandas as pd
import numpy as np

st.title("データ変換アプリ")
st.caption('水文統計ユーティリティに入力するデータセットを作成します。')
st.caption('*注 年別合計データファイル（01_SUM_Y.csv）をインプットして下さい!!!')
with st.form(key='resample_form'):

    upfile = st.file_uploader("ファイルアップロード",type ='csv')
    submit_btn = st.form_submit_button('データ変換')
    if submit_btn:                      #取得開始処理
        st.text("データ変換中") 
        swich = 0 #今年のデータ含まれるかどうかの判定 
        df = pd.read_csv(upfile, header=0, names=["day","rain(mm)","Temp","windspeed(m/s)","suntime(h)"])
        
        day = pd.to_datetime(df['day']).dt.year
        rain = df['rain(mm)'].values
        
        #水文統計ユーティリティ入力データセット作成
        # line 01
        Line01 = 'VER2'
        # line 03
        Line03 = '-9999 0'
        #line04 ~
        maxyer = max(day)
        minyer = min(day)
        yer = np.arange(minyer,maxyer+1,1)
        if swich == 1:
            yer = yer[:-1]
        stryer = list(yer-1)
        strrain = list(yer-1)
        
        for i in range(len(yer)):
            dam00 = str(yer[i])
            stryer[i] = dam00 + "/01/01 "
            strrain[i] = str(rain[i])
        
        # line 02
        dam = str(len(yer))
        Line02 = dam + " 水系１ " + "水系２"
        # output file
        st.text("**********  *.dat形式で保存   ***********")
        st.text(Line01)
        st.text(Line02)
        st.text(Line03)
        for i in range(len(yer)):
            Line04 = stryer[i] + strrain[i]
            st.text(Line04)
        st.text("*******************************")
