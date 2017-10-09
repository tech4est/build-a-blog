from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(200))
    blog_body = db.Column(db.Text)
    
    def __init__(self, blog_title, blog_body):
        self.blog_title = blog_title
        self.blog_body = blog_body

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('newpost.html', title="Add Blog Entry")

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        title_error = ""
        body_error = ""

        if blog_title == "":
            title_error = "Please fill in the title"
        
        if blog_body == "":
            body_error = "Please fill in the body"

        if title_error == "" and body_error == "":
            new_blog_entry = Blog(blog_title, blog_body)
            db.session.add(new_blog_entry)
            db.session.commit()
            query_param = '/blog?id=' + str(new_blog_entry.id)
            return redirect(query_param)
            
        else:    
            blogs = Blog.query.all()
            return render_template('blog.html', title="Blog Posts", blogs=blogs)

        # else:
        #     return render_template('newpost.html', title='New Post Error', blog_title=blog_title, blog_body=blog_body, title_error=title_error, body_error=body_error) 

@app.route("/blog", methods = ['POST', 'GET'])
def blog():
    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)

        return render_template('blog.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build a Blog", blogs=blogs)    
    
    # blog_title = request.form['blog_title']
    # blog_body = request.form['blog_body']

    # #Do I need to use the blog.query.all in this section?
    # blogs = Blog.query.all()
    # return render_template('blog.html', blog_title=blog_title, blog_body=blog_body)

@app.route("/")
def index():
    return "<h1>Go to the proper route above</h1>"

if __name__ == '__main__':
    app.run()