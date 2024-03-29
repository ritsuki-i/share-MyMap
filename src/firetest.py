import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from User import User

from src.User import User

# ===================== Firebase =====================================
# このPythonファイルと同じ階層に認証ファイル(秘密鍵)を配置して、ファイル名を格納
JSON_PATH = 'static\js\pytest-bf0f6-firebase-adminsdk-8xy33-9a264f3956.json'

# Firebase初期化
cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

collectionName="name" #'name'-->コレクション名
colectionLocate="location" # 'location'-->サブコレクション名
docs_list = [] #<-マップマーカー用辞書のリスト


#Cloud Firestoreのコレクションに個人のデータを格納
def setUser(User):
    doc_ref=db.collection(collectionName).document(User.UserID)
    doc_ref.set({
        u'Email': User.UserEmail,
        u'Id': User.UserID
    })
    
    
#Cloud Firestoreのサブコレクションにマーカー情報を格納
def save_marker_to_firestore(marker_info,Id):
    db = firestore.client()
    markers_ref = db.collection(collectionName).document(Id).collection(colectionLocate)  

    # マーカー情報をFirestoreに保存
    markers_ref.add({
        'label': marker_info['label'],
        'lat': marker_info['lat'],
        'lng': marker_info['lng'],
        'description': marker_info['description']
    })

#Cloud Firestoreのサブコレクションにある全てのドキュメントの情報をすべて取得
def get_allmarker_from_firestore(Id):
    docs = db.collection(collectionName).document(Id).collection(colectionLocate).stream()
    for doc in docs:
        #Firestoreから取得したドキュメントを辞書のリストとして格納
        docs_list.append(doc.to_dict())
        #print(f"{doc.id} => {doc.to_dict()}")
    print(docs_list)
    return docs_list  #全てのドキュメントの情報を辞書のリスト形式で返す
        
#Cloud Firestoreのサブコレクションにある各ドキュメントの情報をすべて取得
def get_marker_from_firestore(Id,LocationId):
    doc_ref = db.collection(collectionName).document(Id).collection(colectionLocate).document(LocationId)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return doc.to_dict #ドキュメントの情報を辞書形式で返す
    else:
        print("No such document!")


        
#ex

User=User()
User.UserID="15822097" #<-自動で割当？ 
User.UserEmail="15822097@aoyama.jp"

Lname="Shinjuku"
lat=135
lng=68
description="hitoippai"
#マップマーカーの辞書
marker= {"label": Lname, "lat": lat, "lng": lng, "description": description}
LocationId="IZ0JM1G5m8bHOWLCNgP7"

setUser(User)
save_marker_to_firestore(marker,User.UserID)
get_allmarker_to_firestore(User.UserID)
get_marker_to_firestore(User.UserID,LocationId)

