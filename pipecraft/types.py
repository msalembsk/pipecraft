from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ResourceData:
    data: Dict[str, List[str]]

    def validate(self) -> bool:
        return all(isinstance(v, list) for v in self.data.values())
