D0_list =[[0.899,0.889,0.878,0.867,0.855,0.843,0.830,0.817,0.802,0.787,0.770,0.752],
          [0.941,0.935,0.929,0.922,0.915,0.908,0.900,0.893,0.884,0.875,0.865,0.855],
          [0.997,0.996,0.996,0.995,0.994,0.993,0.992,0.991,0.990,0.989,0.988,0.986],
          [1.055,1.060,1.065,1.070,1.076,1.081,1.087,1.093,1.100,1.107,1.115,1.123],
          [1.104,1.114,1.123,1.134,1.144,1.156,1.167,1.180,1.193,1.208,1.223,1.240],
          [1.129,1.141,1.153,1.166,1.180,1.194,1.209,1.225,1.242,1.261,1.280,1.302],
          [1.118,1.129,1.140,1.152,1.164,1.177,1.191,1.206,1.221,1.237,1.255,1.274],
          [1.077,1.084,1.091,1.098,1.106,1.114,1.123,1.132,1.141,1.151,1.162,1.174],
          [1.022,1.024,1.025,1.027,1.029,1.031,1.033,1.035,1.037,1.039,1.041,1.045],
          [0.964,0.960,0.956,0.952,0.947,0.942,0.938,0.932,0.927,0.921,0.915,0.909],
          [0.913,0.904,0.895,0.885,0.875,0.865,0.854,0.842,0.830,0.817,0.803,0.787],
          [0.887,0.875,0.863,0.850,0.838,0.824,0.809,0.794,0.778,0.760,0.742,0.721],
          [0.942,0.936,0.930,0.923,0.916,0.909,0.902,0.894,0.885,0.877,0.867,0.857]] #２月うるう年



from ssl import HAS_NEVER_CHECK_COMMON_NAME
import streamlit as st
import pandas as pd
import base64
import numpy as np
from PIL import Image

st.title("Hamon法")
st.caption('日別気温データから蒸発散量を換算するアプリ(******* 開発中 *******)')
with st.form(key='resample_form'):

    upfile = st.file_uploader("ファイルアップロード",type ='csv')
    lat =st.text_input('北緯')
    submit_btn = st.form_submit_button('データ変換')
    if submit_btn:                      #取得開始処理
        st.text("データ変換中") 
        #dfinput = pd.read_csv(upfile, index_col='day', parse_dates=True)
        dfinput = pd.read_csv(upfile, header=0, names=["day","rain(mm)","Temp","windspeed(m/s)","suntime(h)"])
        day = pd.to_datetime(dfinput['day'])
        month = pd.to_datetime(dfinput['day']).dt.month
        Temp = dfinput['Temp'].values
        rain = dfinput['rain(mm)'].values
        
        nday = len(Temp)
        
        hamon = np.empty(nday)     #結果集計用配列
        
        
        result = pd.DataFrame(hamon)
        result.columns = ['Ep']
        
        result_tank = result
        result_tank['snow'] = ''
        result_tank.insert(0,"rain(mm)",rain)
        result_tank.insert(0,"Temp",Temp)
        result_tank.insert(0,"day",day)
        result_tank = result_tank[["day","Temp","rain(mm)",'snow','Ep']]

        print(result_tank)
        
        csv01 = result_tank.to_csv(index=False)
        b64_01 = base64.b64encode(csv01.encode()).decode()
        href_01 = f'<a href="data:application/octet-stream;base64,{b64_01}" download="Tank_dataset.csv">download_link</a>'  
        st.markdown(f"タンクモデル用データセット => {href_01}",unsafe_allow_html=True)  

        


image = Image.open('Hamon.png')
st.image(image, caption='ハーモン法の月別可照時間D0（12時間/1日）',use_column_width=True)


