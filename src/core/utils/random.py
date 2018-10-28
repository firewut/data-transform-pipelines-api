import random
import string
import uuid


def random_bool():
    return bool(random.getrandbits(1))


def random_int(_min: int, _max: int):
    return random.randint(_min, _max)


def random_float(_min: int, _max: int):
    return random.uniform(_min, _max)


def random_string(N: int = 10):
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase
        ) for _ in range(N)
    )


def random_uuid4():
    return str(uuid.uuid4())
