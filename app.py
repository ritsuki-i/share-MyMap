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
@app.route('/my-map', methods=['GET','POST'])
def map_page():
    def map_page():
        # Default values for latitude and longitude
        default_lat = 35.6764
        default_lng = 139.6500

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'search_location':
                location = request.form.get('location')
                lat_lng = get_lat_lng(location) if location else (default_lat, default_lng)
                lat, lng = lat_lng if lat_lng else (default_lat, default_lng)
            elif form_type == 'submit_location':
                lat, lng = request.form.get('lat'), request.form.get('lng')
                name = request.form.get('name')
                description = request.form.get('description')
                map_marker = {"label": name, "lat": lat, "lng": lng, "description": description}
                return render_template("main.html", lat=lat, lng=lng, map_marker=map_marker,
                                       google_map_key=GOOGLE_MAP_KEY)
            else:
                lat, lng = default_lat, default_lng
        else:
            # GET request or no form submission: use default values
            lat, lng = default_lat, default_lng

        return render_template("main.html", lat=lat, lng=lng, google_map_key=GOOGLE_MAP_KEY, map_marker=None)
    
if __name__ == "__main__":
    app.run(debug=True)