import face_recognition
import numpy as np
from io import BytesIO




def is_same_person(
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


    if not first_image_encoding or not second_image_encoding:
        return False, 0


    if not isinstance(first_image_encoding, list) or not isinstance(second_image_encoding, list):
        raise ValueError("Both encodings must be of type 'list'.")

    first_image_encoding = np.array(first_image_encoding)
    second_image_encoding = np.array(second_image_encoding)


    face_distance = face_recognition.face_distance([first_image_encoding], second_image_encoding)[0]
    print(face_distance)
    
    is_same_person = face_distance <= threshold
    confidence = 1 - face_distance
    
    return is_same_person, confidence


def encode_image(image):
    byte_image = face_recognition.load_image_file(BytesIO(image))
    encoding = face_recognition.face_encodings(byte_image)

    if encoding:
        return encoding[0].tolist()

    else:
        return []
