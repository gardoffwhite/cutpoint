from flask import Flask, render_template, request, session, redirect
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # เข้าสู่ระบบผ่าน nage-warzone
        login_url = "http://nage-warzone.com/admin/login.php"
        session_data = requests.Session()
        res = session_data.post(login_url, data={"username": username, "password": password})

        if "Logout" in res.text:
            session["logged_in"] = True
            session["session_data"] = session_data.cookies.get_dict()
            return redirect("/charedit")

        return render_template("login.html", error="Login Failed")

    return render_template("login.html")


@app.route('/charedit', methods=["GET", "POST"])
def charedit():
    if not session.get("logged_in"):
        return redirect("/")

    if request.method == "POST":
        charname = request.form['charname']
        payload = {"charname": charname}

        session_data = requests.Session()
        session_data.cookies.update(session["session_data"])

        res = session_data.post("http://nage-warzone.com/admin/charedit.php", data=payload)
        return res.text  # ส่งผลลัพธ์ตรงๆ กลับมาที่เว็บ

    return render_template("charedit.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
