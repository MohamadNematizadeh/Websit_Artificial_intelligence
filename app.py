
import os
import cv2
import numpy as np
from pydantic import ValidationError



from flask import Flask, flash, render_template, request, redirect, url_for, session as flask_session
from sqlmodel import Field, SQLModel, create_engine, Session, select
from PIL import Image
from datetime import datetime 


from model import User,RegisterModel,Comment,LoginModel
from data import get_user_by_username,create_user,verify_password,engine
from src.face_analysis import FaceAnalysis
import base64


def encode_image(image):
    _, buffer = cv2.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    image_uri = f'data:image/png;base64,{image_base64}'
    return image_uri

app = Flask("Face_Analyez")

app.config['UPLOAD_FOLDER'] = 'static/uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey'

face_analysis = FaceAnalysis("models/det_10g.onnx", "models/genderage.onnx")

def relative_time(data_time):
      input_time = datetime.strptime(data_time,'%Y-%m-%d %H:%M:%S.%f')
      current_time = datetime.now()
      time_differ = current_time - input_time 
      seconds = time_differ.total_seconds()
      if seconds <60:
            return f"{int(seconds)} seconds ago "
      elif seconds <3600:
            return f"{int(seconds // 60)} minutes ago"
      elif seconds <86400:
            return f"{int(seconds // 3600)} hours ago"
      else:
            return f"{int(seconds // 86400)} days ago"
      
def allowed_file(file):
     return True
# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        password = data.get("password")
        confirmpassword = data.get("confirmpassword")

        if password != confirmpassword:
            flash("Passwords do not match", "#ab0a0a")
            return render_template('register.html')

        try:
            register_data = RegisterModel(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                username=data.get("username"),
                age=data.get("age"),
                city=data.get("city"),
                country=data.get("country"),
                password=password
            )
        except ValidationError as e:
            flash("Password is incorrect", "#ab0a0a")
            return render_template('register.html', error=str(e))

        if get_user_by_username(register_data.username):
            flash("Username already exists", "#ab0a0a")
            return render_template('register.html', error='')
        
        create_user(register_data)

        flash("Your register done successfully", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/logout")
def logout():
    flask_session.pop("user_id")
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.form
        try:
            login_data = LoginModel(username=data['username'], password=data['password'])
        except ValidationError as e:
            flash("Type error", "yellow")
            return render_template('login.html', error=str(e))

        user = get_user_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.password_hash):
            return render_template('login.html', error='Invalid credentials')
        
        flash("Welcome, you are logged in")
        flask_session["user_id"] = user.id
        return redirect(url_for('service'))
    flash("Password is incorrect", "#ab0a0a")
    

@app.route("/upload", methods=['GET', 'POST'])
def upload():
     if flask_session.get('user_id'):
        if request.method == "GET":
            return render_template("upload.html")
        elif request.method == "POST":
            input_image_file = request.files['image']
            if input_image_file.filename == "":
                return redirect(url_for('upload'))
            else:
                if input_image_file and allowed_file(input_image_file.filename):
                    input_image = Image.open(input_image_file.stream)
                    input_image = np.array(input_image)
                    input_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2RGB)

                    output_image, genders, ages = face_analysis.detect_age_gender(input_image)
                    image_uri = encode_image(output_image)

                    return render_template("result.html", genders=genders, ages=ages, image_uri=image_uri)
        else:
            return redirect(url_for("index"))
           

@app.route("/BMR",methods=['GET','POST'])
def  calculator_BMR():
    if request.method == "GET":
        return render_template("BMR_Calculator.html")
    elif request.method == "POST":
        gender = request.form["gender"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        age = float(request.form["age"])
        
        if gender == "Male":
            bmr =  66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
            print(bmr)

        elif gender == "Female":
            bmr =  655.1 + (9.563 * weight ) + (1.850 * height) - (4.676 * age)
            print(bmr)
        else:
            return "Invalid gender. Please select 'Male' or 'Female'."
        
        return render_template("bmr_result.html", bmr=bmr)



@app.route("/mediapipe")
def mediapipe():
    
    return render_template("mediapipe.html")
@app.route("/admin")
def admin():
    with Session(engine) as db_session:
        statement = select(User)
        users = list(db_session.exec(statement))
    return render_template("admin.html" , users=users)


@app.route("/admin_users")
def admin_user():
    with Session(engine) as db_session:
        statement = select(User)
        users = list(db_session.exec(statement))
        for user in users:
            user.jon_time = relative_time(data_time=user.jon_time)
        
    return render_template("admin_users.html",users=users)

@app.route("/admin_comment")
def admin_comment():
      if request.method == "GET":
        with Session(engine) as db_session:
            statement = select(Comment)
            comments = list(db_session.exec(statement))
            for comment in comments:
                print(comment)
            return render_template("admin_comment.html",comments=comments)


@app.route("/service", methods=['GET'])
def service():
      if request.method == "GET":
        with Session(engine) as db_session:
            statement = select(Comment)
            comments = list(db_session.exec(statement))
            for comment in comments:
                print(comment)
            return render_template("service.html",comments=comments)


@app.route("/add-new-comment", methods=['POST'])
def add_new_comment():
    if request.method == "POST":
        text = request.form["text"]
        with Session(engine) as db_session:
            new_comment = Comment(user_id=flask_session.get('user_id'), content=text)
            db_session.add(new_comment)
            db_session.commit()

            return redirect(url_for("service"))

if __name__ == '__main__':
    app.run(debug=True)
