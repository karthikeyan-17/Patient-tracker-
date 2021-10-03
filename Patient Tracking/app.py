from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from DB_Opr import pat_insert, pat_get, pat_get_act, pat_details, pat_search, pat_search_ac, pat_login, pat_dashboard, pat_comp, rep_insert, rep_get, case_add, \
    case_comp, case_get
import os
from werkzeug.utils import secure_filename
import random
from datetime import datetime as dt
from datetime import timedelta
import pywhatkit as pt
import pytz

app = Flask(__name__)
app.secret_key = "123@abc"
app.config['UPLOAD_FOLDER'] = "upload"
Username = "Admin"
Password = "123456"
Login = False


def set_session(no):
    """
    Setting Session of the Patient
    :param no: Patient Id
    :return:
    """
    session["logged_in"] = True
    session["no"] = no


def reset_session():
    """
    Resetting the Session
    :return:
    """
    if "logged_in" in session:
        del session["logged_in"]
        del session["no"]


def verify_login(name, password):
    """
    Verification of the Login Procedures for Admin
    :param name: Admin name
    :param password: Password
    :return:
    """
    global Password, Username, Login

    if password == Password and name == Username:
        Login = True
        return redirect("/admin")
    else:
        flash("Wrong Username/Password")
        return redirect("/login_a")


def verify_login_p(no, dob):
    """
    Verification of Login for Patients
    :param no: Patient Id
    :param dob: Patient DOB
    :return:
    """
    str_dob = pat_login(no)
    if len(str_dob):
        if dob == str_dob[0][0]:
            set_session(no)
            return redirect("/patient")
        else:
            flash("Incorrect DOB or Id ")
            return redirect("/login_p")
    else:
        flash("Incorrect DOB or Id ")
        return redirect("/login_p")


@app.route("/login_a", methods=["GET", "POST"])
def login_a():
    """
    Login Template
    :return:
    """
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        name = request.form["name"]
        password = request.form["pwd"]
        verify_login(name, password)
        return redirect(url_for("admin"))


@app.route("/login_p", methods=["GET", "POST"])
def login_p():
    """
    Login Template
    :return:
    """
    if request.method == "GET":
        return render_template('login_p.html')
    elif request.method == "POST":
        no = request.form["no"]
        dob = request.form["dob"]
        verify_login_p(no, dob)
        return redirect(url_for("patient"))


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Adding Patients into Database
    :return:
    """
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        name = request.form["name"]
        adr = request.form["adr"]
        city = request.form["city"]
        state = request.form["state"]
        con = request.form["opt"]
        gen = request.form["gender"]
        dob = request.form["dob"]

        try:
            f = request.files['file']
            file = f.filename
            val = file.split(".")
            a = str(random.randrange(1000, 5000))
            file = a + "-" + val[0] + "." + val[1]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file)))
        except IndexError:
            file = "None"
        IST = pytz.timezone('Asia/Kolkata')
        now = dt.now(IST)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        no = name[0:4] + str(random.randrange(2500, 5000))
        case_add()
        pat_insert(no, name, adr, city, state, con, gen, file, dt_string, dob)
        return redirect("/admin")


@app.route("/view", methods=["GET", "POST"])
def view():
    """
    Viewing All the Patients in the Database
    :return:
    """
    if request.method == "GET":
        no, name, dt = pat_get()
        dat = []
        for i in range(len(name)):
            dat.append(dt[i][0].split())
        return render_template("view.html", length=len(name), no=no, name=name, date=dat)
    elif request.method == "POST":
        if request.form['btn'] == 'View':
            text = request.form["text"]
            name, gen, city, con, att, date, dob, val = pat_details(text)
            rep, dt_upl = rep_get(text)
            if len(rep):
                upl = True
            else:
                upl = False
            if att[0][0] == "None":
                return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=False,
                                       gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                                       dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
            else:
                return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=True,
                                       gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                                       dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
        else:
            key = request.form["key"]
            print("got")
            if key != "":
                print("in")
                name, dt, no = pat_search(key)
                dat = []
                for i in range(len(name)):
                    dat.append(dt[i][0].split())
                return render_template("view.html", length=len(name), no=no, name=name, date=dat)
            else:
                return redirect("/view")


@app.route("/active", methods=["GET", "POST"])
def active():
    """
    Viewing the Active Patients in the Database
    :return:
    """
    if request.method == "GET":
        no, name, dt = pat_get_act(0)
        dat = []
        for i in range(len(name)):
            dat.append(dt[i][0].split())
        return render_template("view.html", length=len(name), no=no, name=name, date=dat)
    elif request.method == "POST":
        if request.form['btn'] == 'View':
            text = request.form["text"]
            name, gen, city, con, att, date, dob, val = pat_details(text)
            rep, dt_upl = rep_get(text)
            if len(rep):
                upl = True
            else:
                upl = False
            if att[0][0] == "None":
                return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=False,
                                       gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                                       dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
            else:
                return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=True,
                                       gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                                       dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
        else:
            key = request.form["key"]
            if key != "":
                name, dt, no = pat_search_ac(key, 0)
                dat = []
                for i in range(len(name)):
                    dat.append(dt[i][0].split())
                return render_template("view.html", length=len(name), no=no, name=name, date=dat)
            else:
                return redirect("/active")


@app.route("/complete", methods=["GET", "POST"])
def complete():
    """
    Viewing the Completed Patients in the Database
    :return:
    """
    if request.method == "GET":
        no, name, dt = pat_get_act(1)
        dat = []
        for i in range(len(name)):
            dat.append(dt[i][0].split())
        return render_template("view.html", length=len(name), no=no, name=name, date=dat)
    elif request.method == "POST":
        if request.form['btn'] == 'View':
            text = request.form["text"]
            name, gen, city, con, att, date, dob, val = pat_details(text)
            rep, dt_upl = rep_get(text)
            if len(rep):
                upl = True
            else:
                upl = False
            if att[0][0] == "None":
                return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=False,
                                       gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                                       dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
            else:
                return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=True,
                                       gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                                       dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
        else:
            key = request.form["key"]
            if key != "":
                name, dt, no = pat_search_ac(key, 1)
                dat = []
                for i in range(len(name)):
                    dat.append(dt[i][0].split())
                return render_template("view.html", length=len(name), no=no, name=name, date=dat)
            else:
                return redirect("/complete")


@app.route("/download", methods=["POST"])
def download():
    """
    Downloading Files
    :return:
    """
    text = request.form["att_val"]
    return send_file("upload/" + text, as_attachment=True)


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    """
    Setting the Dashboard for the User
    :return:
    """
    if request.method == "GET":
        date, att, con = pat_dashboard(session["no"])
        rep, dt_upl = rep_get(session["no"])
        _, _, _, _, _, _, _, val = pat_details(session["no"])
        if len(rep):
            upl = True
        else:
            upl = False
        if con[0][0] == "PSI":
            apt = dt.strptime(date[0][0], '%d/%m/%Y %H:%M:%S') + timedelta(weeks=4)
            apt = apt.strftime("%d/%m/%Y")
        else:
            apt = dt.strptime(date[0][0], '%d/%m/%Y %H:%M:%S') + timedelta(weeks=2)
            apt = apt.strftime("%d/%m/%Y")
        return render_template("pat_dash.html", no=session["no"], date=date, att=att[0][0], con=con, apt=apt, rep=rep,
                               dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
    else:
        try:
            f = request.files['file']
            file = f.filename
            val = file.split(".")
            a = str(random.randrange(1000, 5000))
            file = a + "-" + val[0] + "." + val[1]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file)))
        except IndexError:
            file = "None"
        IST = pytz.timezone('Asia/Kolkata')
        now = dt.now(IST)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        rep_insert(session["no"], file, dt_string)
        return redirect("/dashboard")


@app.route("/cases", methods=["POST"])
def cases():
    """
    Marking Case as Complete
    :return:
    """
    case_comp()
    text = request.form["text"]
    pat_comp(text)
    name, gen, city, con, att, date, dob, val = pat_details(text)
    rep, dt_upl = rep_get(text)
    if len(rep):
        upl = True
    else:
        upl = False
    if att[0][0] == "None":
        return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=False,
                               gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                               dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])
    else:
        return render_template("pat_det.html", name=name[0][0], no=text, con=con[0][0], att=att[0][0], atth=True,
                               gen=gen[0][0], dob=dob[0][0], date=date[0][0].split()[0], city=city[0][0], rep=rep,
                               dt_upl=dt_upl, upl=upl, length=len(rep), val=val[0][0])


@app.route("/chat", methods=["POST", "GET"])
def chat():
    """
    Chat Option
    :return:
    """
    pt.sendwhatmsg_instantly("+918608244017", "Hi")
    name, gen, city, con, _, _, dob, _ = pat_details(session["no"])
    return render_template("pat_log.html", no=session["no"], name=name[0][0], gen=gen[0][0], city=city[0][0],
                           con=con[0][0], dob=dob[0][0])


@app.route("/logout_a")
def logout_a():
    """
    Logging Out
    :return:
    """
    global Login
    Login = False
    return redirect("/")


@app.route("/logout_p")
def logout_p():
    """
    Logging Out
    :return:
    """
    reset_session()
    return redirect("/")


@app.route("/", methods=["POST", "GET"])
def home():
    """
    Home Page
    :return:
    """
    if request.method == "GET":
        act, com, tot = case_get()
        return render_template("index.html", act=act[0][0], com=com[0][0], tot=tot[0][0])
    else:
        if request.form['btn'] == 'Admin':
            return redirect(url_for('admin'))
        else:
            reset_session()
            return redirect(url_for('patient'))


@app.route("/admin")
def admin():
    """
        Admin Login Page
        :return:
        """
    global Login
    if Login:
        act, com, tot = case_get()
        return render_template('doc.html', act=act[0][0], com=com[0][0], tot=tot[0][0])
    else:
        return redirect(url_for('login_a'))


@app.route("/patient")
def patient():
    """
    Patient Login Page
    :return:
    """
    if "logged_in" in session:
        name, gen, city, con, _, _, dob, _ = pat_details(session["no"])
        return render_template("pat_log.html", no=session["no"], name=name[0][0], gen=gen[0][0], city=city[0][0],
                               con=con[0][0], dob=dob[0][0])
    else:
        return redirect(url_for('login_p'))


if __name__ == '__main__':
    app.run(debug=True)
