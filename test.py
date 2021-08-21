from mlBackend import walkingML

ml = walkingML()

user_data = ml.fetch_firebase("chat")
user_data = ml.fillData(user_data)
result = ml.detect(user_data)
ml.setResult(result,"entry/1234")
print("Succcess!")
