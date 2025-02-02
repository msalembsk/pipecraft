import itertools
from functools import wraps
from pathlib import Path
from string import Template
from typing import Callable

from pipecraft.factory import ExtractorFactory, ResourceProvider
from pipecraft.types import ResourceData


def extractor_config(
    source_name: str,
    extractor_type: str,
    url_template: str,
    output_pattern: str,
    resources: ResourceProvider = None,
    **options,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            params = []
            if resources:
                resource_data = resources.get_resources()
                # Generate combinations from resource data
                params = [
                    {
                        k.rstrip("s"): v
                        for k, v in zip(resource_data.data.keys(), values)
                    }
                    for values in itertools.product(*resource_data.data.values())
                ]

            extractor = ExtractorFactory.create(
                extractor_type=extractor_type,
                source_name=source_name,
                url_template=url_template,
                **options,
            )

            responses = extractor.extract_batch(params)
            param_response_pairs = zip(params, responses)

            results = []
            for param, response in param_response_pairs:
                output_path = Template(output_pattern).safe_substitute(**param)
                full_path = Path(output_path).resolve()
                full_path.parent.mkdir(parents=True, exist_ok=True)

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(response)

                results.append(str(full_path))

            return results

        return wrapper

    return decorator


def resources(func: Callable[[], ResourceData]) -> ResourceProvider:
    return ResourceProvider(func)
