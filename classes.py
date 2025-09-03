class Request:
    text: str

    @staticmethod
    def from_json(data: dict) -> 'Request | None':
        request = Request()
        request.text = data.get('text', '')
        if not request.text:
            return None
        return request


class Response:
    text: str

    def serialize(self) -> dict:
        return {'text': self.text}


class Debug:
    iteration: int
    text: str
    tools: dict

    def serialize(self) -> dict:
        return {
            'iteration': self.iteration,
            'text': self.text,
            'tools': self.tools
        }
