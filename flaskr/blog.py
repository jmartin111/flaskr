from flask import (
    Blueprint, g, request, redirect, url_for, flash, render_template
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """This view is the 'homepage' and will display
       all posts that have been submitted
    """
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        "   FROM post p JOIN user u on p.author_id = u.id"
        "   ORDER BY created DESC"
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "A title must be supplied"

        if error:
             flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)"
                "   VALUES (?, ?, ?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/index.html')


def get_post(post_id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, body, created, author_id, username"
        "   FROM post p JOIN user u on p.author_id = u.id"
        "   WHERE p.id = ?",
        (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id [{post_id}] doesnt exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_post():
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

    if not title:
        error = "Title is required"

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            "UPDATE post SET title = ?, body = ?"
            "   WHERE id = ?",
            (title, body, id)
        )
        db.commit()
        return redirect(url_for('blog.index'))

    render_template('blog/update.html', post=post)
