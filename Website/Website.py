
import json
from flask import Flask, redirect, url_for, render_template, request, Response
import cv2
import os

os.chdir('/Shared/Python_Projects/Room_Lights/Website/')


app = Flask(__name__, template_folder='./templates')

disp = True

logged_in_users = {}

user = False

with open('Logins/Trusted-ips.json', 'r') as fp:
    trusted_ips = json.load(fp)

with open('Logins/Users.json', 'r') as fp:
    users = json.load(fp)


def register_user(username, password: str):
    with open('Logins/Users.json', 'r+') as fp:
        users[username] = password
        json.dump(users, fp)


def add_ip(ip):
    with open('Logins/Trusted-ips.json', 'r+') as fp:
        trusted_ips[ip] = 1
        json.dump(trusted_ips, fp)


@app.route('/')
def home():
    return render_template("Home.html")


@app.route('/login')
def login():
    return render_template("Login.html", )


@app.route('/login', methods=['POST'])
def verify_login():
    username = request.form['username']
    password = request.form['password']
    if username in users:
        if users[username] == password:
            if request.form.get('stay_logged_in'):
                add_ip(request.remote_addr)
            logged_in_users[request.remote_addr] = True
            print(trusted_ips)
            if username == 'Ugo Novello':
                user = True
            return redirect(url_for("home"))
    return redirect(url_for("login"))


def gen_frames():
    while True:
        camera = cv2.VideoCapture(0)
        camera.set(3, 1280)
        camera.set(4, 720)
        success, frame = camera.read()
        camera.release()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/lights', methods=['POST'])
def lights():
    red = request.values['Red']
    return render_template("Lights.html", red=red)


@app.route('/lights')
def red():
    return redirect(url_for("lights"))


@app.route('/discord', methods=['GET', 'POST'])
def discord():
    global disp
    if disp:
        state = 'On'
    else:
        state = 'Off'
    return render_template("Discord.html", display_state=state)


@app.route('/discord')
def reboot():
    print('restarted')
    return redirect(url_for("discord"))


@app.route('/display')
def display():
    global disp
    disp = not disp
    return redirect(url_for("discord"))


@app.route('/display-mode', methods=['GET', 'POST'])
def display_mode():
    mode = request.values['select-display']
    return redirect(url_for("discord"))


@app.route('/reload-api', methods=['GET', 'POST'])
def reload_api():
    api = request.form['API_KEY']
    print(api)
    return redirect(url_for("discord"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("Page_Not_Found.html")


@app.route('/Tests')
def test():
    return render_template("balises html.html")


@app.before_request
def ensure_login():
    if request.endpoint not in ['login', 'verify_login', 'page_not_found', 404]:
        ip = request.remote_addr
        if ip in trusted_ips:
            logged_in_users[ip] = True
        elif ip in logged_in_users:
            pass
        else:
            return redirect(url_for("login"))

@app.before_request
def user_check():
    if request.endpoint not in ['video', 'login', 'verify_login', 'page_not_found', 404]:
        if user != True:
            return redirect(url_for("video"))


"""
@app.route('/exit')
def exit():
    print('hello')
    return redirect(url_for('user', name='me'))


@app.route('/')
def home():
    return redirect(url_for('admin'))


@app.route('/user/<name>')
def user(name):
    return name

@app.route('/admin')
def admin():
    return render_template("GUI.html", f=10)
"""

app.run(host="192.168.0.163", port=5000)
