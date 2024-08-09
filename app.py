from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlmodel import Session, select
from model import User, Comment, Topic,RegisterModel , LoginModel
from data import get_user_by_username, create_user, verify_password, engine
from pydantic import ValidationError
import datetime
from io import BytesIO
import base64

import requests
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app = Flask("AI Web App")
app.secret_key = "my_secret_key"
app.config["UPLOAD_FOLDER"] = "./uploads"

ai_face_analysis_microservice_url = "https://pydeploy-zv3n.onrender.com/analyze-face"
def relative_time(data_time):
    if isinstance(data_time, str):
        data_time = datetime.strptime(data_time, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    time_difference = current_time - data_time
    seconds = time_difference.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minutes ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hours ago"
    else:
        days = int(seconds // 86400)
        return f"{days} days ago"
    

def truncate_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    else:
        truncated = text[:max_length].rsplit(' ', 1)[0]
        return truncated + '...'



# Routes
@app.route('/')
def index():
    return render_template('index.html')

# User Routes
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

# Service Roytes

@app.route("/service", methods=['GET'])
def service():
      if request.method == "GET":
        with Session(engine) as db_session:
            statement = select(Comment)
            comments = list(db_session.exec(statement))
            for comment in comments:
                print(comment)
            return render_template("service/service.html",comments=comments)
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/service/detect-age-gender", methods=['GET', 'POST'])
def upload():
    if flask_session.get('user_id'):
        if request.method == "GET":
            return render_template("service/upload.html")
        elif request.method == "POST":
            input_image_file = request.files['image']
            if input_image_file.filename == "":
                return redirect(url_for('upload'))
            else:
                if input_image_file and allowed_file(input_image_file.filename):
                    print("Sending image to FastAPI service...")
                    response = requests.post(
                        ai_face_analysis_microservice_url,
                        files={"file": input_image_file},
                    )
                    print(f"Response received: {response.status_code}")
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        genders = response_data.get("genders")
                        ages = response_data.get("ages")
                        image_base64 = response_data.get("image")
                        
                        if not genders or not ages or not image_base64:
                            flash("Incomplete response from the service.", "warning")
                            return redirect(url_for("upload"))
                        
                        return render_template(
                            "service/result.html", 
                            genders=genders, 
                            ages=ages,
                            image_base64=image_base64
                        )
                    else:
                        flash("Error processing image.", "danger")
                        return redirect(url_for("upload"))
                else:
                    flash("File type not allowed. Please upload a PNG, JPG, or JPEG image.", "danger")
                    return redirect(url_for("upload"))
    else:
        flash("Please log in to access this service.", "danger")
        return redirect(url_for('login'))
           

@app.route("/service/BMR",methods=['GET','POST'])
def  calculator_BMR():
    if request.method == "GET":
        return render_template("service/BMR_Calculator.html")
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
        
        return render_template("service/bmr_result.html", bmr=bmr)

@app.route("/service/mediapipe")
def mediapipe():
    return render_template("service/mediapipe.html")


@app.route("/service/comment/add-new-comment", methods=['POST'])
def add_new_comment():
    if request.method == "POST":
        text = request.form["text"]
        with Session(engine) as db_session:
            new_comment = Comment(user_id=flask_session.get('user_id'), content=text)
            db_session.add(new_comment)
            db_session.commit()
            return redirect(url_for("service"))


#Admin Route

@app.route("/admin")
def admin():
    user_id = flask_session.get('user_id')
    role = flask_session.get('role')
    if not user_id:
        return redirect(url_for('login'))
    
    with Session(engine) as db_session:
        statement = select(User)
        users = list(db_session.exec(statement))
    return render_template("admin/admin.html" , users=users)

@app.route("/admin/users")
def admin_user():
    with Session(engine) as db_session:
        statement = select(User)
        users = list(db_session.exec(statement))
        # for user in users:
        #     user.jon_time = relative_time(user.jon_time)
        
    return render_template("admin/admin_users.html", users=users)

@app.route("/admin/comment")
def admin_comment():
      if request.method == "GET":
        with Session(engine) as db_session:
            statement = select(Comment)
            comments = list(db_session.exec(statement))
            for comment in comments:
                print(comment)
            return render_template("admin/admin_comment.html",comments=comments)


@app.route("/admin/blog", methods=['GET', 'POST'])
def admin_blog():
    if request.method == "GET":
        with Session(engine) as db_session:
            topics = list(db_session.exec(select(Topic)))
        return render_template("admin/admin_blog.html", topics=topics)

@app.route("/admin/blog/add-new-blog", methods=['POST'])
def add_new_blog():
    title = request.form["title"]
    text = request.form["text"]
    with Session(engine) as db_session:
        new_topic = Topic(user_id=flask_session.get('user_id'), text=text, title=title, timestamp=datetime.now())
        db_session.add(new_topic)
        db_session.commit()
    return redirect(url_for("admin_blog"))


@app.route("/admin/blog/del/<int:id>", methods=['POST'])
def del_blog(id):
    with Session(engine) as db_session:
        topic_to_delete = db_session.get(Topic, id)
        if topic_to_delete:
            db_session.delete(topic_to_delete)
            db_session.commit()
    return redirect(url_for("admin_blog"))

@app.route("/admin/blog/edit", methods=['POST'])
def edit_blog():
    topic_id = request.form["id"]
    title = request.form["title"]
    text = request.form["text"]
    with Session(engine) as db_session:
        topic_to_edit = db_session.get(Topic, topic_id)
        if topic_to_edit:
            topic_to_edit.title = title
            topic_to_edit.text = text
            db_session.commit()
    return redirect(url_for("admin_blog"))
    

# Bloog Route    
@app.route("/blog/")
def blog():
    with Session(engine) as db_session:
        statement = select(Topic)
        topics = list(db_session.exec(statement))
        for topic in topics:
            topic.timestamp = relative_time(topic.timestamp)
            topic.text = truncate_text(topic.text)
    return render_template("blog.html", topics=topics)

@app.route("/blog/<int:topic_id>")
def blog_topic(topic_id):
    with Session(engine) as db_session:
        topics = db_session.query(Topic).filter_by(id=topic_id).first()   
    return render_template("topic.html", topic=topics)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
