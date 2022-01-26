import markdown2

from projects.workers.base import Worker


class Markdown(Worker):
    id = "markdown"
    name = "markdown"
    image = "https://steemitimages.com/0x0/http://markdown-here.com/img/icon256.png"
    description = "Render an html from a markdown"
    schema = {
        "type": "object",
        "properties": {
            "in": {"type": "string", "description": "raw markdown"},
            "out": {"type": "string", "description": "markdown'ed :D"},
        },
    }

    def process(self, data):
        return markdown2.markdown(data)
