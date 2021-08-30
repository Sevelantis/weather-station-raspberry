import json

class DTO:
    def __init__(self) -> None:
        pass
    
    def serialize(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
    def deserialize(self, msg: str) -> None:
        self.__dict__ = json.loads(msg)