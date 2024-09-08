from flask import Flask, request
from flask_mysqldb import MySQL
from os import getenv
import detector


app = Flask(__name__)

# TODO externalize these data to be secured
app.config["MYSQL_HOST"] = "db"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "finder"

mysql = MySQL(app)


MEDIA_FOLDER = getenv("MEDIA_FOLDER", "media/")
app.config["MEDIA_FOLDER"] = MEDIA_FOLDER


def get_images_and_ids_from_db() -> tuple:
    cur = mysql.connection.cursor()
    cur.execute("SELECT image, id FROM finder_app_contact where image is not null")
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/", methods=["POST"])
def index():
    source_image = request.files["image"].read()
    data = get_images_and_ids_from_db()

    found_ids = []

    for image, id in data:
        if not image:
            continue
        second_image_path = f"{MEDIA_FOLDER}/{image}"
        with open(second_image_path, "rb") as f:
            second_image = f.read()
            if detector.is_same_person(source_image, second_image):
                found_ids.append(id)


    return str(found_ids)
