import random
import string
import uuid
import os
import io

from PIL import Image


def random_bool():
    return bool(random.getrandbits(1))


def random_int(_min: int, _max: int):
    return random.randint(_min, _max)


def random_float(_min: int, _max: int):
    return random.uniform(_min, _max)


def random_string(N: int = 10, alphabet: str = None):
    if not alphabet or not isinstance(alphabet, str):
        alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits

    return "".join(random.SystemRandom().choice(alphabet) for _ in range(N))


def random_uuid4():
    return str(uuid.uuid4())


def random_image(width=500, height=500):
    def ran():
        return os.urandom(width * height)

    image = Image.new("RGB", [width, height])
    pixels = zip(ran(), ran(), ran())
    image.putdata(list(pixels))

    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format="PNG")

    return image_byte_array
