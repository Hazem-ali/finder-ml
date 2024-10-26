from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from os import getenv
import detector
import json

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
    cur.execute("SELECT id, encoding FROM image_encodings where encoding is not null")
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/", methods=["POST"])
def index():
    source_image = request.files["image"].read()
    source_image_encoding = detector.encode_image(source_image)

    if source_image_encoding is None:
        return -1

    data = get_images_and_ids_from_db()

    found_ids = {}

    for id, db_image_encoding in data:
        if not db_image_encoding:
            continue

        is_same_person, confidence = detector.is_same_person(
            source_image_encoding, json.loads(db_image_encoding)
        )

        if is_same_person:
            found_ids[id] = float(confidence)

    return jsonify(found_ids)


@app.route("/images/encode", methods=["POST"])
def encode():
    source_image = request.files["image"].read()

    encoded_image = detector.encode_image(source_image)
    if encoded_image is None:
        encoded_image = ""

    return jsonify(encoded_image)


@app.route("/contacts/save", methods=["POST"])
def save():
    contact_id = request.json["id"]
    encoded_image = request.json["encoded_image"]

    if encoded_image is None:
        return "No face encoding provided.", 400

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM image_encodings WHERE id = %s", (contact_id,))
    record = cur.fetchone()

    if record:
        cur.execute(
            "UPDATE image_encodings SET encoding = %s WHERE id = %s",
            (json.dumps(encoded_image), contact_id),
        )
        mysql.connection.commit()
        response = f"Updated encoding for contact ID {contact_id}"
    else:
        cur.execute(
            "INSERT INTO image_encodings (id, encoding) VALUES (%s, %s)",
            (contact_id, json.dumps(encoded_image)),
        )
        mysql.connection.commit()
        response = f"Inserted new encoding for contact ID {contact_id}"

    cur.close()

    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
