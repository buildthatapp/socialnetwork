from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from socialnetwork import db
from socialnetwork.models import Post
from socialnetwork.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():

        post = Post(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(post)
        db.session.commit()
        flash("Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


@posts.route('/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, date=post.date, post=post)


@posts.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('posts.post', blog_post_id=post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@posts.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))