from flask import Flask, redirect, render_template, request, jsonify
from src.User import User
from src.lat_lng_finder import get_lat_lng

app = Flask(__name__)
User = User()

GOOGLE_MAP_KEY = "AIzaSyBKOqBE1tCLB4_ruwU8WVyCuDRN0exE_xo"

@app.route('/', methods=['GET'])
def login():
    if request.method == 'GET':
        User.UserEmail =  None
        User.UserID =  None
        return render_template(
        'login.html'
    )
    else:
        return render_template(
            'login.html'
        )
    

@app.route('/toMyMap', methods=['GET','POST'])
def toMyMap():
    if request.method == 'GET':
        if User.UserEmail !=  None and User.UserID !=  None:
            return render_template(
                'mymap.html', UserEmail=User.UserEmail, UserID=User.UserID
            )
        else:
            return render_template(
            'login.html'
            )
    else:
        UserData = request.json
        print(type(UserData))
        User.UserEmail = UserData['User']['email']
        User.UserID = UserData['User']['uid']
        return redirect('/my-map')
    
@app.route('/CreateAccount', methods=['GET','POST'])
def CreateAccount():
    return render_template(
        'createAccount.html'
    )

# 2024/3/18 Ian
# static/js/map.js, templates/mymap.html, src/lat_lng_finder.py, app.pyのmap_page()を追加
# 今の時点でデータベースに入れるのは[ 緯度, 経度, ユーザが入力した名前, ユーザが入力したデスクリプション ]
# データベースはまだ設定されていないから、今まだ一個のマーカーしか見せないようにしている。
@app.route('/my-map', methods=['GET','POST'])
def map_page():
    # デフォルトの緯度と経度を設定
    default_lat = 35.6764
    default_lng = 139.6500

    if request.method == 'POST':
        # フォームの種類を取得
        form_type = request.form.get('form_type')

        if form_type == 'search_location':
            # ユーザーが入力した場所名から緯度と経度を検索
            location = request.form.get('location')
            lat_lng = get_lat_lng(location) if location else (default_lat, default_lng)
            lat, lng = lat_lng if lat_lng else (default_lat, default_lng)
        elif form_type == 'submit_location':
            # ユーザーがフォームに入力した緯度、経度、名前、説明を取得
            lat, lng = request.form.get('lat'), request.form.get('lng')
            name = request.form.get('name')
            description = request.form.get('description')
            # マップマーカーの情報を辞書で作成
            map_marker = {"label": name, "lat": lat, "lng": lng, "description": description}
            # テンプレートに変数を渡してレンダリング
            return render_template("mymap.html", lat=lat, lng=lng, map_marker=map_marker,
                                   google_map_key=GOOGLE_MAP_KEY)
        else:
            # それ以外のPOSTリクエストではデフォルト値を使用
            lat, lng = default_lat, default_lng
    else:
        # GETリクエストの場合はデフォルト値を使用
        lat, lng = default_lat, default_lng

    # マップページを表示。初期値または検索結果をマップに反映
    return render_template("mymap.html", lat=lat, lng=lng, google_map_key=GOOGLE_MAP_KEY, map_marker=None)

    
if __name__ == "__main__":
    app.run(debug=True)