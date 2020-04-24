
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
                          
class ChampionPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  role = db.Column(db.String(50), nullable=False)
  stats = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  abilities = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(20), nullable=False, default='N/A')
  postdate = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow))
  
  def __repr__(self):
    return 'Champion entry ' + str(self.id)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
  if request.method == 'POST':
    post_title = request.form['title']
    post_role = request.form['role']
    post_stats = request.form['stats']
    post_content = request.form['content']
    post_abilities = request.form['abilities']
    post_author = request.form['author']
    post_picture = request.form['picture']
    new_post = ChampionPost(title=post_title, role=post_role, stats=post_stats,
                            content=post_content, abilities=post_abilities, author=post_author)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else: 
    all_posts = ChampionPost.query.order_by(ChampionPost.postdate).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
  post = ChampionPost.query.get_or_404(id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  post = ChampionPost.query.get_or_404(id)
  if request.method == 'POST':
    post.title = request.form['title']
    post.role = request.form['role']
    post.stats = request.form['stats']
    post.content = request.form['content']
    post.abilities = request.form['abilities']
    post.author = request.form['author']
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('edit.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def posts2():
  if request.method == 'POST':
    post_title = request.form['title']
    post_role = request.form['role']
    post_stats = request.form['stats']
    post_content = request.form['content']
    post_abilities = request.form['abilities']
    post_author = request.form['author']
    post_picture = request.form['picture']
    new_post = ChampionPost(title=post_title, role=post_role, stats=post_stats,
                            content=post_content, abilities=post_abilities, author=post_author)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('newpost.html')

if __name__ == "__main__":
  app.run(debug=True)
