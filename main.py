from flask import Flask, render_template, request,redirect

from flask_login import LoginManager


import pymysql
import pymysql.cursors

login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)


class User:
     def _init_(self, id, username, banned):
          self.is_authenticated = True 
          self.is_anonymous = False
          self.is_active = not banned 
    

          self.username = username 
          self.id = id 

def get_id(self):
     return str(self.id)


connection = pymysql.connect(
    host = "10.100.33.60",
    user = "bwilliams",
    password = "244727137",
    database= "bwilliams_social_media",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit = True
)

@login_manager.user_loader
def user_loader(user_id):
     cursor = connection.cursor()

     cursor.execute("SELECT * from `users` WHERE `id` = " + user_id)

     result = cursor.fetchone()

     if result is None:
          return None
     
     return User(result['id,'],result["username"],result ["banned"])

@app.route("/")
def index():
    return render_template ("home.html.jinja")

@app.route( '/feed')

def post_feed():
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM  `posts` ORDER BY `TimeStamp`")

    results = cursor.fetchall()

    return render_template(
        "feed.html.jinja",
        posts=results
    )
@app.route('/sign-in')
def sign_in():
     return render_template("sign_in.html.jinja")

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():

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
        
        return request.form 
    
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")


if __name__=='__main__':
        app.run(debug=True)

