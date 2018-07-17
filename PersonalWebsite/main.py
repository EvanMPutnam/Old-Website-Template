from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import markdown
import os
import utils.UserManager
from flask_login import LoginManager




#NOTE default user/pass is admin admin


'''
Boot up python
    from main import db
    db.create_all()
    db.session.commit()
    
pip install flask
pip install sqlalchemy
pip install flask-login
pip install Markdown
'''


#App config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['UPLOAD_FOLDER'] = 'static/ImageUploads'
app.secret_key = "Spex42069Lolroflcopters"
#Handle db
db = SQLAlchemy(app)

#Handle login
login_manager = LoginManager()
login_manager.init_app(app)

from model import *


@login_manager.user_loader
def loadUser(user_id):
    '''
    Loads in the user.
    :param user_id:
    :return:
    '''
    return User.query.filter_by(id=user_id).one()



@app.route("/allAdminPages")
@login_required
def adminPanel():
    return render_template("adminPage.html", current_user=current_user.username)



#TODO Limit login attempts for brute force attacks.
@app.route("/loginPlox", methods=["GET", "POST"])
def login():
    '''
    Login to check if users are who they say they are
    :return:
    '''
    #Get the form
    form = LoginForm()
    #If validated
    if form.validate_on_submit():
        try:
            #Try to get the user, if fail then error.
            user = User.query.filter_by(username=form.userName.data, password=utils.UserManager.hashPass(form.password.data)).one()
        except:
            return "Invalid login"
        #Try to login the user
        login_user(user)

        #Render the home page!
        posts = BlogPost.query.filter_by().order_by("-id")
        return render_template("index.html", blogs=posts)

    #Otherwise render login again
    return render_template("login.html", form=form)

@app.route("/logoutPlox")
@login_required
def logout():
    '''
    Logs out the user from the web server.
    :return:
    '''
    logout_user()
    return "You are no longer logged in"



@app.route("/someUserData")
@login_required
def testLogin():
    '''
    Just a test function to display login information
    :return:
    '''
    return "The current user is "+current_user.username


@app.route('/portfolio')
def portfolioPost():
    try:
        posts = PortfolioPost.query.filter_by()
        return render_template("portfolio.html", posts=posts)
    except:
        return "Error in loading blog posts"


@app.route('/about')
def about():
    return render_template("about.html")

@login_required
@app.route('/preview', methods=['POST'])
def previewPost():
    content = request.form['content']
    mDown = markdown.markdown(content)

    title = request.form['title']
    author = request.form['author']
    image = request.form['imagePreview']

    post = BlogPost(content=mDown, author=author, title=title, image=image)
    return render_template("blog.html", post=post)




@app.route('/blog')
def blog():
    if request.args.get('postId') != None:
        try:
            post = BlogPost.query.filter_by(id=request.args['postId']).one()
            return render_template("blog.html", post=post)
        except:
            return "404 Error be here"

    posts = BlogPost.query.filter_by().order_by("-id")
    return render_template("blog.html", posts=posts)



@app.route('/contact')
def contactMe():
    return render_template("contact.html")

@app.route('/')
def index():
    posts = BlogPost.query.filter_by().order_by("-id")
    return render_template("index.html", blogs=posts)

@login_required
@app.route('/uploadPost')
def uploadPost():
    return render_template("uploadPost.html")


@login_required
@app.route('/images')
def uploadedImages():
    images = os.listdir(os.path.join(app.static_folder, "ImageUploads"))
    return render_template("images.html", images = images)


@login_required
@app.route('/deleteBlog/<path:id>')
def deleteBlogDialog(id):
    try:
        blogPost = BlogPost.query.filter_by(id=id).first()
        db.session.delete(blogPost)
        db.session.commit()
    except:
        return "Error in delete"
    return "Success"

@app.route('/deletePortfolio/<path:id>')
@login_required
def deletePortfolioDialog(id):

    try:
        portPost = PortfolioPost.query.filter_by(id=id).first()
        db.session.delete(portPost)
        db.session.commit()
    except:
        return "Error in delete"

    return "Success"


@login_required
@app.route("/deleteItem")
def deleteItem():
    portfolioPosts = PortfolioPost.query.filter_by().order_by("-id")
    blogPosts = BlogPost.query.filter_by().order_by("-id")
    return render_template("deletePost.html", posts=blogPosts, portfolios=portfolioPosts)


@login_required
@app.route('/uploadImage', methods=['POST'])
def uploadPhoto():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    print(f)
    file.save(f)
    return render_template("uploadPost.html")


@login_required
@app.route('/addPost', methods=['POST'])
def addPost():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    image = request.form['imagePreview']
    print(image)

    portBool = "off"
    if "portfolio" in request.form:
        portBool = request.form['portfolio']

    blogBool = "off"
    if "blog" in request.form:
        blogBool = request.form['blog']

    mDown = markdown.markdown(content)

    if blogBool == "on":
        post = BlogPost(title=title, author=author, content=mDown, date=datetime.datetime.now(), image=image)
        db.session.add(post)
        db.session.commit()
    if portBool == "on":
        post = PortfolioPost(title=title, author=author, content=mDown, date=datetime.datetime.now(), image=image)
        db.session.add(post)
        db.session.commit()

    return "Upload success"



if __name__ == '__main__':
    app.run(debug=False)