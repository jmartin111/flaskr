"""This is a Flask Blueprint
It is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application,
they are registered with a blueprint. Then the blueprint is registered
with the application when it is available in the factory (__init__) function.
"""
from datetime import datetime
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
        "SELECT p.id, title, body, created, updated_on, author_id, username"
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
        updated_on = None
        error = None

        if not title:
            error = "A title must be supplied"

        if error:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, updated_on, author_id)"
                "   VALUES (?, ?, ?, ?)",
                (title, body, updated_on, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(post_id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, body, created, updated_on, author_id, username"
        "   FROM post p JOIN user u on p.author_id = u.id"
        "   WHERE p.id = ?",
        (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id [{post_id}] doesnt exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update_post(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        updated_on = datetime.utcnow()  # rendered to local time on the client-side
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, updated_on = ?'
                ' WHERE id = ?',
                (title, body, updated_on, post_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:post_id>/delete', methods=('GET', 'POST'))
@login_required
def delete_post(post_id):
    db = get_db()
    db.execute("DELETE from post WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for('blog.index'))
