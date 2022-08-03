
import streamlit as st
import pandas as pd
import base64
import numpy as np
from PIL import Image

# 初期データセット

hokui_list = np.array([24,26,28,30,32,34,36,38,40,42,44,46])

D0_list =np.array([[0.899,0.889,0.878,0.867,0.855,0.843,0.830,0.817,0.802,0.787,0.770,0.752],
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
                   [0.942,0.936,0.930,0.923,0.916,0.909,0.902,0.894,0.885,0.877,0.867,0.857]]) #２月うるう年

print(D0_list[7,2])

uru_list = np.array([1904,1908,1912,1916,1920,1924,1928,1936,1940,1944,1948,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,
                     2004,2008,2012,2016,2020,2024,2028,2032,2026,2040,2044,2028,2052,2056,2060,2064,2068,2072,2076,2080,2084,2088,2092,2096])

alpha = 7.5
beta  = 237.3

# GUI処理

st.title("Hamon法")
st.caption('日別気温データから蒸発散量を換算するアプリ(******* 開発中 *******)')
with st.form(key='resample_form'):

    upfile = st.file_uploader("ファイルアップロード",type ='csv')
    hokui =st.text_input('北緯 (24 ~ 46)')
    option = st.selectbox('select box:',["水面上","氷面上"])
    submit_btn = st.form_submit_button('データ変換')
    
    if submit_btn:                      #取得開始処理
        st.text("データ変換中  **データ欠測は0℃で換算します**") 
        if option == "水面上":
            alpha = 7.5
            beta  = 237.3  
        if option == "氷面上":
            alpha = 9.5
            beta  = 265.3  
            
        lat = float(hokui)
         
        # 入力データの処理
        dfinput = pd.read_csv(upfile, header=0, names=["day","rain(mm)","Temp","windspeed(m/s)","suntime(h)"])
        day = pd.to_datetime(dfinput['day'])
        year = pd.to_datetime(dfinput['day']).dt.year
        month = pd.to_datetime(dfinput['day']).dt.month
        Temp0 = dfinput['Temp'].values
        Temp = np.where(np.isnan(Temp0), 0, Temp0)
        rain = dfinput['rain(mm)'].values
        
        nday = len(Temp)
                
        #　北緯処理 インデックスとズレを検索
        index = np.abs(lat - hokui_list).argsort()[0].tolist()
        per = (lat - hokui_list[index])/2.0   #hokui_listが2刻み
        
        if per <= 0:
            index0 = index - 1
        if per > 0:
            index0 = index + 1
        
        Ep    = np.empty(nday)  #日可能蒸発散能
        D0    = np.empty(nday)  #可照時間
        asatG = np.empty(nday)  #飽和絶対湿度
        asatP = np.empty(nday)  #飽和水蒸気圧
        
        for i in range(nday):   #可照時間の処理
            if month[i] == 2 and year[i] in uru_list:
                month[i] = 13
            M = month[i] -1
            err = D0_list[[M],index] - D0_list[[M],index0]
            D0[i] = D0_list[[M],index] + err * per
        
        asatP = 6.1078 * 10 ** (alpha * Temp / (beta + Temp))
        asatG = 0.2167 * (asatP / (Temp + 273.15)) * 1000
        Ep    = 0.14 * (D0 * D0) * asatG
        
        for i in range(nday):
            print(day[i],Temp[i],asatP[i],asatG[i],D0[i],Ep[i])
        
        #出力処理
        result = pd.DataFrame(Ep)
        result.columns = ['Ep']
        result_tank = result
        
        result.insert(0,"D0(12h/day)",D0)
        result.insert(0,"asat(g/m3)",asatG)
        result.insert(0,"esat(hpa)",asatP)
        result.insert(0,"temp",Temp)
        result.insert(0,"Time",day)
        
        csv00 = result.to_csv(index=False)
        b64_00 = base64.b64encode(csv00.encode()).decode()
        href_00 = f'<a href="data:application/octet-stream;base64,{b64_00}" download="Hamon_result.csv">download_link</a>'  
        st.markdown(f"Hamon計算結果 => {href_00}",unsafe_allow_html=True)  

        result_tank['snow'] = ''
        result_tank.insert(0,"rain(mm)",rain)
        result_tank.insert(0,"Temp",Temp)
        result_tank.insert(0,"day",day)
        result_tank = result_tank[["day","Temp","rain(mm)",'snow','Ep']]

#        print(result_tank)
        
        csv01 = result_tank.to_csv(index=False)
        b64_01 = base64.b64encode(csv01.encode()).decode()
        href_01 = f'<a href="data:application/octet-stream;base64,{b64_01}" download="Tank_dataset.csv">download_link</a>'  
        st.markdown(f"タンクモデル用データセット => {href_01}",unsafe_allow_html=True)  

        


image = Image.open('Hamon.png')
st.image(image, caption='ハーモン法の月別可照時間D0（12時間/1日）',use_column_width=True)


