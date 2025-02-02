from typing import Callable

from .extractors.api import APIExtractor
from .extractors.web import WebExtractor
from .types import ResourceData


class ExtractorFactory:
    @staticmethod
    def create(extractor_type: str, **kwargs):
        extractors = {
            "api": APIExtractor,
            "web": WebExtractor,
            #'file': FileExtractor,
            #'bigquery': BigQueryExtractor,
            #'postgres': PostgresExtractor
        }

        extractor_class = extractors.get(extractor_type)
        if not extractor_class:
            raise ValueError(f"Unsupported extractor type: {extractor_type}")

        return extractor_class(**kwargs)


class ResourceProvider:
    def __init__(self, func: Callable[[], ResourceData]):
        self.func = func
        self._resources = None

    def get_resources(self) -> ResourceData:
        if self._resources is None:
            self._resources = self.func()
            if not self._resources.validate():
                raise ValueError("Invalid resource data structure")
        return self._resources
