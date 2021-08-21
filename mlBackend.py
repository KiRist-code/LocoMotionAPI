from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation
import numpy as np
from numpy import argmax
import joblib
from tensorflow.python.keras.models import load_model
from tensorflow.keras import Model
import pandas as pd
import firebase_admin
from firebase_admin import db, credentials

class walkingML:
    def initialize(self):
        # Firebase database 인증 및 앱 초기화
        cred = credentials.Certificate('./MLBackEnd/chat-547bd-firebase-adminsdk-p4h8k-0d34c24703.json')
        firebase_admin.initialize_app(cred,{
            'databaseURL' : 'https://chat-547bd-default-rtdb.firebaseio.com/'
        })
        
        firebase_admin.get_app()
        
        dir = db.reference() # 기본 위치 지정
    
    def fetch_firebase(self, db_dir):
        dir = db.reference(db_dir)
        data=dir.get()

        dic=list(data.values())
        dic=dic[0]
        df_user=pd.DataFrame(dic['ux'])
        df_user=df_user.transpose()
        return df_user

    def fillData(self, df_user):
        if df_user.shape[1] > 450 :
            df_user=df_user.loc[:,:449]
        else : 
            for i in range(df_user.shape[1],450) :
                df_user[i] = 0.0
        return df_user
        
    def detect(self, df_user):
        file_name='./MLBackEnd/scaler_locomotion.pkl'
        scaler=joblib.load(file_name)

        model = load_model('locomotion.h5')

        userdata_scaled=scaler.transform(df_user)

        pred = model.predict(userdata_scaled)

        pred= (pred> 0.5)
        pred=pred.tolist()
        result=pred[0].index(True)
        print(result)
        return result

    def setResult(self,result,db_dir):
        dir = db.reference()
        dir = db.reference(db_dir)
        dir.set(result)
