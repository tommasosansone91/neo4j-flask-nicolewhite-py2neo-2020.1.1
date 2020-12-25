from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import User, todays_recent_posts

#aggiungo io
from py2neo import Graph, NodeMatcher
from .models import graph

app = Flask(__name__)
app.secret_key = "['VpN.R#}e3e5(eB"

@app.route("/")
def index():
    posts = todays_recent_posts(5)
    return render_template("index.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User(username)

        if not user.register(password):
            flash("Esiste già un altro user con quell'username.", "error")
        else:
            flash("Utente registrato con successo!")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User(username)

        if not user.verify_password(password):
            flash("username o password errati", "error")
        else:
            flash("Login effettuato!")
            session["username"] = user.username
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/add_post", methods=["POST"])
def add_post():
    title = request.form["title"]
    tags = request.form["tags"]
    text = request.form["text"]

    # flask session object tracks users across requests
    user = User(session["username"])

    #controllo duplicati dei post, sul titolo e sul test
    matcher = NodeMatcher(graph)

    if not title or not tags or not text:
        flash("Il post deve avere titolo, tags e testo.", "error")    

    elif matcher.match('Post', text=text).first():
        flash("Esiste già un altro post con questo identico testo, per favore cambia il testo.", "error")

    # elif matcher.match('Post', title=title).first():
    #     flash("Esiste già un altro post con questo identico titolo, per favore cambia il titolo.", "error")


    else:
        user.add_post(title, tags, text)
        flash("Post pubblicato!") 

    return redirect(url_for("index"))






@app.route("/like_post/<post_id>")
def like_post(post_id):
    return "TODO"


@app.route("/profile/<username>")
def profile(username):
    return "TODO"


@app.route("/logout")
def logout():
    return "TODO"