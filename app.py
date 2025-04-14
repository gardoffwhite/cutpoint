from flask import Flask, render_template, request, session, redirect
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ข้อมูลล็อกอิน
login_url = "http://nage-warzone.com/admin"
edit_url = "http://nage-warzone.com/admin/charedit.php"
admin_user = "admin"
admin_pass = "3770"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        session_data = requests.Session()
        res = session_data.post(login_url, data={
            "username": admin_user,
            "password": admin_pass,
            "submit": "Submit"
        })

        print("Login Status Code:", res.status_code)
        print("Login Response Snippet:", res.text[:500])

        if "Logout" in res.text:
            session["logged_in"] = True
            session["session_data"] = session_data.cookies.get_dict()
            return redirect("/charedit")

        return render_template("login.html", error="Login Failed")

    return render_template("login.html")


@app.route('/charedit', methods=["GET", "POST"])
def charedit():
    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":
        charname = request.form['charname']
        str_value = request.form['str']
        dex_value = request.form['dex']
        int_value = request.form['int']
        money_value = request.form['money']

        session_data = requests.Session()
        session_data.cookies.update(session["session_data"])

        session_data.post(edit_url, data={
            "charname": charname,
            "searchname": "Submit"
        })

        postData = {
            "lv": "",
            "exp": "",
            "eclv": "",
            "ecexp": "",
            "str": str_value,
            "dex": dex_value,
            "int": int_value,
            "money": money_value,
            "lvpoint": "",
            "skpoint": "",
            "esp": "",
            "lic": "",
            "spt": "",
            "bankmoney": "",
            "cmap": "",
            "hero": "",
            "x": "",
            "y": "",
            "z": "",
            "update": "Update"
        }

        res = session_data.post(f"{edit_url}?charname={charname}", data=postData)
        return res.text

    return render_template("charedit.html")


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    session.pop("session_data", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
