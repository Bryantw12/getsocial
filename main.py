from flask import Flask, render_template, request, redirect , send_from_directory

from flask_login import LoginManager, login_required, login_user, current_user, logout_user


import pymysql
import pymysql.cursors

login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'something_random'


class User:
     def __init__(self, id, username, banned):
          self.is_authenticated = True
          self.is_anonymous = False
          self.is_active = not banned

          self.username = username
          self.id = id

     def get_id(self):
          return str(self.id)


connection = pymysql.connect(
    host="10.100.33.60",
    user="bwilliams",
    password="244727137",
    database="bwilliams_social_media",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


@login_manager.user_loader
def user_loader(user_id):
     cursor = connection.cursor()

     cursor.execute("SELECT * from `users` WHERE `id` = " + user_id)

     result = cursor.fetchone()

     if result is None:
          return None

     return User(result['id'], result["username"], result["banned"])


@app.get('/media/<path:path>')
def send_media(path):
    return send_from_directory('media',path)


@app.route("/")
def index():
    return render_template("home.html.jinja")


@app.route('/feed')
@login_required
def post_feed():

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM  `posts` ORDER BY `TimeStamp`")

    results = cursor.fetchall()

    return render_template(
        "feed.html.jinja",
        posts=results
    )

@app.route('/post', methods=['POST'])
@login_required
def create_post():
     cursor = connection.cursor

     photo = request.files['photo']

     file_name = photo.filename

     file_extension = file_name.split('.')[-1]

     if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
             photo.save('media/posts/' + file_name)
        
     else:
          raise Exception('Invalid file type')

     user_id = current_user.id

     cursor.execute("INSERT INTO `users` (`post_text`, `post_image`, `user_id`) ")

     return redirect('/feed')


@app.route('/sign-out')
def sign_out():
     logout_user()

     return redirect('/sign-in')


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
     if current_user.is_authenticated:
       return redirect('/feed')

     if request.method == 'POST':

          cursor = connection.cursor()

          cursor.execute(f"SELECT * FROM `users` WHERE `username` =  '{request.form ['username']}' ")

          result = cursor.fetchone()

          if result is None:
               return render_template("sign_in.html.jinja")

          if request.form['password'] == result['password']:
              user = User(result['id'], result['username'], result['banned'])

              login_user(user)

              return redirect('/feed')

          else:
               return render_template("sign_in.html.jinja")

          return request.form

     elif request.method == 'GET':
          return render_template("sign_in.html.jinja")


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():

     if current_user.is_authenticated:
        return redirect('/feed')


     if request.method =='POST':
       
        cursor = connection.cursor()

        photo = request.files ['photo']

        file_name = photo.filename

        file_extension = file_name.split('.')[-1]

        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
             photo.save('media/users' + file_name)
        
        else:
             raise Exception('Invalid file type')

        cursor.execute(""""
        INSERT INTO `users`(`username` , `email` , `display_name` , `password` , `bio` , `photo`,  `birthday`)
        VALUES(%s, %s, %s, %s, %s, %s)
    
         """,(request.form['Username'], request.form['email_address'],request.form['dispay_name'],request.form['password'],request.form['bio'],file_name,request.form['birthday']))

        return redirect('/post')
     elif request.method == 'GET':

        return render_template("sign.up.html.jinja")


if __name__=='__main__':
         app.run(debug=True)

