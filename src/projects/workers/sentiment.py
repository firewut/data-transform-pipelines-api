from textblob import TextBlob

from projects.workers.base import Worker


class Sentiment(Worker):
    id = 'sentiment'
    name = 'sentiment'
    image = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/146/thinking-face_1f914.png'
    description = 'Sentiment analysis aims to determine the attitude of a speaker or a writer with respect to some topic or the overall contextual polarity of a text'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": [
                    "string"
                ],
                "description": "text to analyze"
            },
            "out": {
                "type": "number",
                "description": "polarity of a text"
            }
        }
    }

    def process(self, data):
        self.processor.check_input_data(data)

        blobbed = TextBlob(data)
        sentiment = blobbed.sentiment

        return sentiment.polarity
