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

        # จำลอง login ด้วย requests หรือ cURL
        login_url = "http://nage-warzone.com/admin/login.php"
        session_data = requests.Session()
        res = session_data.post(login_url, data={"username": username, "password": password})

        if "Logout" in res.text:
            session["logged_in"] = True
            session["session_data"] = session_data.cookies.get_dict()
            return redirect("/charedit")

        return "Login Failed"

    return '''
        <form method="POST">
            <input name="username" placeholder="Username"><br>
            <input name="password" placeholder="Password" type="password"><br>
            <button type="submit">Login</button>
        </form>
    '''

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
        return res.text

    return '''
        <form method="POST">
            <input name="charname" placeholder="Character Name"><br>
            <button type="submit">Submit</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
