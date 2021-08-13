from flask import (
    Blueprint, g, request, redirect, url_for, flash, render_template
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.index('/')
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        "   FROM post p JOIN user u on p.author = u.id"
        "   ORDER BY created DESC"
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.create('/create', methods=('GET', 'POST'))
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
                "INSERT INTO post (title, body, author_id"
                "   VALUES (?, ?, ?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/index.html')
