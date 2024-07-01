import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error("A non-existing article is accessed")
      return render_template('404.html'), 404
    else:
      app.logger.info(f"Article {post[2]} retrieved!")
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('The "About Us" page is retrieved.')
    return render_template('about.html')

@app.route('/healthz')
def health_check():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    if posts:
        response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps({"result":"NOT - healthy"}),
            status=404,
            mimetype='application/json'
        )
    connection.close()
    return response


@app.route('/metrics')
def metrics():
    #initial connection is setup is 0
    connection_count = 0
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    #setting connection count to 1 after first call, not sure if any other way to count the connection
    connection_count = 1
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"db_connection_count":connection_count,"post_count":len(posts)}}),
            status=200,
            mimetype='application/json'
    )
    connection.close()
    return response

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f"A new article {title} is created.")
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
    ## stream logs to app.log file
    logging.basicConfig(datefmt= r'%Y-%m-%d %H:%M:%S %z', filename='app.log',level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')
    
    app.run(host='0.0.0.0', port='3111')
