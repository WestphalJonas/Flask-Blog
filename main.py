from flask import Flask, render_template
import json


app = Flask(__name__)

def get_blog_posts():
    with open("blog_posts.json", "r") as f:
        return json.load(f)

@app.route("/")
def index():
    blog_posts = get_blog_posts()
    return render_template("index.html", posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
