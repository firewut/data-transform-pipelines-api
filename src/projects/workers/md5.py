import hashlib

from projects.workers.base import Worker


class Md5(Worker):
    id = 'md5'
    name = 'md5'
    image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTt1_9m8xZV9PELfJkp5_z5_xsv9F7rSN4KorcrrrXHThXmPTJC'
    description = 'Calculate a message-digest fingerprint (checksum)'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": "string",
                "description": "string to hash"
            },
            "out": {
                "type": "string",
                "description": "Hashed string. Will be pasted to a property where this processor attached"
            }
        }
    }

    def process(self, data):
        str_data = str(data)
        return hashlib.md5(
            str_data.encode('utf-8')
        ).hexdigest()
