from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ResourceData:
    def __init__(self, data: dict, combination_type: str = "simple"):
        self.data = data
        self.combination_type = combination_type
        
    def validate(self) -> bool:
        if self.combination_type == "multiple":
            return all(isinstance(v, list) for v in self.data.values())
        elif self.combination_type == "simple":
            return isinstance(self.data, list) and all(isinstance(x, dict) for x in self.data)
        return False