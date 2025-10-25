from flask import Flask, redirect, render_template, request
import json


app = Flask(__name__)


def get_blog_posts():
    with open("blog_posts.json", "r") as f:
        return json.load(f)


def save_blog_posts(posts):
    with open("blog_posts.json", "w") as f:
        json.dump(posts, f, indent=2)


def add_blog_post(title, content, author):
    posts = get_blog_posts()
    if posts:
        last_id = posts[-1]["id"]
    else:
        last_id = 0
    new_post = {
        "id": last_id + 1,
        "author": author,
        "title": title,
        "content": content,
        "likes": 0,
    }
    posts.append(new_post)
    save_blog_posts(posts)


def update_post(post_id, title, content, author):
    posts = get_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            post["title"] = title
            post["content"] = content
            post["author"] = author
            break
    save_blog_posts(posts)


def fetch_post_by_id(post_id):
    posts = get_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            return post


@app.route("/")
def index():
    blog_posts = get_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = request.form.get("author")

        add_blog_post(title, content, author)
        return redirect("/")
    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    blog_posts = get_blog_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            break
    save_blog_posts(blog_posts)
    return redirect("/")


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = request.form.get("author")

        update_post(post_id, title, content, author)
        return redirect("/")

    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>")
def like_post(post_id):
    posts = get_blog_posts()
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break
    save_blog_posts(posts)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
