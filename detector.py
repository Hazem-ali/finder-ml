import face_recognition
import numpy as np
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



def is_same_person_optimized(
    first_image_encoding: list, second_image_encoding: list, threshold: float = 0.6
) -> bool:
    """
    Compares two face encodings to determine if they belong to the same person.

    Args:
    first_image_encoding (list): The encoding of the first image (from the database or new image).
    second_image_encoding (list): The encoding of the second image (from the database or new image).
    threshold (float): The threshold to determine if the two encodings are close enough to be considered the same person.

    Returns:
    bool: True if the two encodings are similar enough to represent the same person, False otherwise.
    """

    # print(first_image_encoding)
    # print(second_image_encoding)

    if not first_image_encoding or not second_image_encoding:
        return False


    if not isinstance(first_image_encoding, list) or not isinstance(second_image_encoding, list):
        raise ValueError("Both encodings must be of type 'list'.")

    first_image_encoding = np.array(first_image_encoding)
    second_image_encoding = np.array(second_image_encoding)



    face_distance = face_recognition.face_distance([first_image_encoding], second_image_encoding)[0]
    
    # Determine if they are the same person based on the threshold
    is_same_person = face_distance <= threshold

    print(f"Same person? {is_same_person} with error_margin {face_distance}")
    
    return is_same_person


def encode_image(image):
    byte_image = face_recognition.load_image_file(BytesIO(image))
    encoding = face_recognition.face_encodings(byte_image)

    if encoding:
        return encoding[0].tolist()

    else:
        return None
