import streamlit as st
import pandas as pd
import base64
import datetime
import numpy as np

st.title("データ変換アプリ")
st.caption('降雨データを日別累積雨量に換算します。')
with st.form(key='resample_form'):

    upfile = st.file_uploader("ファイルアップロード",type ='csv')
    submit_btn = st.form_submit_button('データ変換')
    if submit_btn:                      #取得開始処理
        st.text("データ変換中") 
        #dfinput = pd.read_csv(upfile, index_col='day', parse_dates=True)
        dfinput = pd.read_csv(upfile, header=0, names=["day","rain(mm)","Temp","windspeed(m/s)","suntime(h)"])
        swich = 0 #今年のデータ含まれるかどうかの判定 
        
        #年毎の加積雨量のグラフを作成　：1.年毎加積曲線（雨量）
        date1 = datetime.datetime.today()
        nowyear = date1.year
        iniy = str(nowyear)
        inid = '-01-01'
        inidate = datetime.datetime.strptime(iniy + inid, '%Y-%m-%d')
        
        daylist = dfinput['day']
        day = pd.to_datetime(dfinput['day']).dt.year
        rain0 = dfinput['rain(mm)'].values
        rain = np.where(np.isnan(rain0), 0, rain0)

        header = np.arange(min(day),max(day)+1,1)
        dy = max(day) - min(day) + 1
        n = len(rain)
        rain_add = np.empty((367,dy + 1))
        
        for i in range(dy):
            rain_add[0,i+1] = 0.0
        
        id = 1
        i1 = 1
        iy = day[0]
        rain_add[1,0] = 1
            
        for i in range(n):
            if iy != day[i]:
                if i1 == 366:
                    rain_add[i1,id] = rain_add[i1-1,id]
                id = id + 1
                iy = day[i]
                i1 = 1
            rain_add[i1,id] = rain_add[i1-1,id] + rain[i]
            i1 = i1 + 1
            rain_add[i1-1,0] = i1-1
            lastday = daylist[i]
        if i1 == 366:
            rain_add[i1,id] = rain_add[i1-1,id]
            id = id + 1
            iy = day[i]
            i1 = 1        

        for i in range(dy):
            rain_add[0,i+1] = header[i]
        
        df = pd.DataFrame(rain_add) 
        csv01 = df.to_csv(index=False)
        b64_01 = base64.b64encode(csv01.encode()).decode()
        href_01 = f'<a href="data:application/octet-stream;base64,{b64_01}" download="ADD_Rain.csv">download_link</a>'  
        st.markdown(f"累積降雨データ => {href_01}",unsafe_allow_html=True)  
        
