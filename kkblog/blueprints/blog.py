from flask import render_template,Blueprint,make_response,abort,current_app,request,flash,redirect,url_for
from kkblog.utils import redirect_back
from flask_login import current_user
from kkblog.models import *
from kkblog.forms import *
from kkblog.emails import *

blog_bp=Blueprint('blog',__name__)

@blog_bp.route("/page/<int:page>")
@blog_bp.route("/",defaults={"page":1})
def index(page):
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config["KKBLOG_POST_PER_PAGE"])
    posts=pagination.items
    return render_template("blog/index.html",pagination=pagination,posts=posts)

@blog_bp.route("/search",defaults={"page":1})
@blog_bp.route("/search/<int:page>")
def search(page):
    question=request.args.get("q")
    if not question:
        flash('Please Input Search Info. By Yuchen', 'info')
        return redirect(url_for('blog.index'))
    pagination=Post.query.filter(Post.title.like('%{keyword}%'.format(keyword=question))).paginate(page,per_page=current_app.config["KKBLOG_POST_PER_PAGE"])
    posts = pagination.items
    return render_template("blog/index.html", pagination=pagination, posts=posts)



@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['KKBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['KKBLOG_EMAIL']
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:  # send message based on authentication status
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            send_new_comment_email(post)  # send notification email to admin
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)



@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")




@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['KKBLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')



@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['KKBLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route("/year/<int:year_id>")
def show_year_category(year_id):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['KKBLOG_POST_PER_PAGE']
    year_articles=Post.query.filter(extract('year', Post.timestamp) == year_id)
    year_articles_list=year_articles.all()
    pagination = year_articles.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts=pagination.items
    return render_template('blog/year_category.html', year=year_id, pagination=pagination, posts=posts,lenths=len(year_articles_list))
