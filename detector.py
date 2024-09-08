import face_recognition
from io import BytesIO


def is_same_person(first_photo, second_photo, threshold=0.6):
    image1 = face_recognition.load_image_file(BytesIO(first_photo))
    image2 = face_recognition.load_image_file(BytesIO(second_photo))

    encoding1 = face_recognition.face_encodings(image1)
    encoding2 = face_recognition.face_encodings(image2)
    if encoding1 and encoding2:
        encoding1 = encoding1[0]
        encoding2 = encoding2[0]

        face_distance = face_recognition.face_distance([encoding1], encoding2)[0]
        is_same_person = face_distance <= threshold
        print(f"Same person? {is_same_person} with error_margin {face_distance}")
        return is_same_person
    else:
        print("Could not find faces in one or both images.")
        return False
