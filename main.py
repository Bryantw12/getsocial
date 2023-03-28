from flask import Flask, render_template, request,redirect
import pymysql
import pymysql.cursors


connection = pymysql.connect(
    host = "10.100.33.60",
    user = "bwilliams",
    password = "244727137",
    database= "bwilliams_social_media",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit = True
)
app = Flask(__name__)


if __name__=='__main__':
        app.run(debug=True)



@app.route("/")
def index():

    return render_template ("home.html.jinja")

@app.route( '/feed')

def post_feed():
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM  `post` ORDER BY `timestamps`")

    results = cursor.fetchall()

    return render_template(
        "feed.html.jinja",
        posts=results
    )