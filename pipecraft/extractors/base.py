from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseExtractor(ABC):
    def __init__(
        self,
        source_name: str,
        save_raw: bool = True,
        output_path: Optional[str] = None,
        retry_attempts: int = 3,
        timeout: int = 30,
    ):
        self.source_name = source_name
        self.save_raw = save_raw
        self.output_path = output_path
        self.retry_attempts = retry_attempts
        self.timeout = timeout

    @abstractmethod
    def extract(self) -> Any:
        pass
