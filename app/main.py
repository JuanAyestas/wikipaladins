
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
                          
class Champion(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  title = db.Column(db.String(50), nullable=False)
  role = db.Column(db.String(20), nullable=False)
  stats = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  abilities = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(20), nullable=False, default='N/A')
  postdate = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow))
  portait = db.Column(db.String(500), nullable=False)
  pictures = db.relationship('Pictures', backref='champion', lazy=True) 
  
  def __repr__(self):
    return 'Champion entry ' + str(self.id)

class Pictures(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  pic_add = db.Column(db.String(300), nullable=False)
  champion_id = db.Column(db.Integer, db.ForeignKey('champion.id'), nullable=False)
  
  def __repr__(self):
    return 'Picture entry ' + str(self.id)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
  all_posts = Champion.query.order_by(Champion.name).all()
  if request.method == 'POST':
    post_name = request.form['name']
    post_title = request.form['title']
    post_role = request.form['role']
    post_stats = request.form['stats']
    post_content = request.form['content']
    post_abilities = request.form['abilities']
    post_author = request.form['author']
    post_portait = request.form['portait']
    new_post = Champion(name= post_name, title=post_title, role=post_role, stats=post_stats,
                            content=post_content, abilities=post_abilities, author=post_author, portait=post_portait)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else: 
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
  post = Champion.query.get_or_404(id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  post = Champion.query.get_or_404(id)
  if request.method == 'POST':
    post.name = request.form['name']
    post.title = request.form['title']
    post.role = request.form['role']
    post.stats = request.form['stats']
    post.content = request.form['content']
    post.abilities = request.form['abilities']
    post.author = request.form['author']
    post.portait = request.form['portait']
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('edit.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def posts2():
  if request.method == 'POST':
    post_name = request.form['name']
    post_title = request.form['title']
    post_role = request.form['role']
    post_stats = request.form['stats']
    post_content = request.form['content']
    post_abilities = request.form['abilities']
    post_author = request.form['author']
    post_portait = request.form['portait']
    new_post = Champion(name=post_name, title=post_title, role=post_role, stats=post_stats,
                        content=post_content, abilities=post_abilities, author=post_author, portait=post_portait)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('newpost.html')

@app.route('/posts/upload/<int:id>', methods=['GET'])
def picture_up(id):
  posts = Champion.query.get_or_404(id)
  if request.method == 'GET':
    return render_template('upload.html', post=posts)

@app.route('/posts/upload', methods=['POST'])
def picture_save():
  if request.method == 'POST':
    posts_pic = request.form['pic_add']
    posts_id = request.form['champion_id']
    new_pic = Pictures(pic_add=posts_pic, champion_id=posts_id)
    db.session.add(new_pic)
    db.session.commit()
    return redirect('/gallery')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
  pics = Pictures.query.order_by(Pictures.champion_id)
  if request.method == 'GET':
    return render_template('gallery.html', pics=pics)
  else:
    return redirect('/gallery')

@app.route('/gallery/<int:id>', methods=['GET', 'POST'])
def gallerychamp(id):
  posts = Champion.query.get_or_404(id)
  pics = Pictures.query.filter(Pictures.champion_id == id)
  if request.method == 'GET':
    return render_template('gallerychamp.html', pics=pics, post=posts)
  else:
    return redirect('/gallery')
