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
            flash("Another user with the same username already exixst. Please chose another one.", "error")
        else:
            flash("User registered!", "success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User(username)

        if not user.verify_password(password):
            flash("Wrong username or password.", "error")
        else:
            session["username"] = user.username
            flash("You logged in as %s!" % session["username"], "success")            
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
        flash("The post must have title, tags and text. Please fill the blank form fields.", "error")    

    elif matcher.match('Post', text=text).first():
        flash("Another post has the same identical text you just typed in. Please change the text of your post.", "error")

    # elif matcher.match('Post', title=title).first():
    #     flash("Esiste già un altro post con questo identico titolo, per favore cambia il titolo.", "error")


    else:
        user.add_post(title, tags, text)
        flash("Post published!", "success") 

    return redirect(url_for("index"))






@app.route("/like_post/<post_id>")
def like_post(post_id):
    username = session.get("username")

    if not username:
        flash("You have to log in in order to like a post.", "error")
        return redirect(url_for("login"))

    user = User(username)
    user.like_post(post_id)
    flash("You just liked a post.", "success")
    return redirect(request.referrer)

    


@app.route("/profile/<username>")
def profile(username):
    user1 = User(session.get("username"))
    user2 = User(username)
    posts = user2.recent_posts(5)

    similar = []

    if user1.username == user2.username:
        similar = user1.similar_users(3)

    return render_template("profile.html", username=username, posts=posts)


@app.route("/logout")
def logout():
    logged_out_user = session.get("username")
    session.pop("username") 
    # è un metodo dei dizionari: ritorna il valore della chiave indicata ed elimina chiave e valore dal dizionario
    flash("%s logged out!" % (logged_out_user), "success" )
    return redirect(url_for("index"))