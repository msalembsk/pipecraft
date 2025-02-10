import itertools
from functools import wraps
from pathlib import Path
from string import Template
from typing import Callable, Union
import yaml
import tomli
import json

from pipecraft.factory import ExtractorFactory, ResourceProvider
from pipecraft.logger.default import get_default_logger
from pipecraft.types import ResourceData


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    
    if path.suffix == '.yaml' or path.suffix == '.yml':
        with open(path, 'r') as f:
            return yaml.safe_load(f)
            
    elif path.suffix == '.toml':
        with open(path, 'rb') as f:
            return tomli.load(f)
            
    elif path.suffix == '.json':
        with open(path, 'r') as f:
            return json.load(f)
            
    raise ValueError(f"Unsupported config format: {path.suffix}")

def extractor_config(
    source_name: str = None,
    extractor_type: str = None,
    url_template: str = None,
    output_pattern: Union[str, Callable] = None,
    resources: ResourceProvider = None,
    config_path: str = None,
    skip_if_exists: bool = False,
    logger_ = None,
    **options
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logger_ or get_default_logger()
            base_config = {}
            if config_path:
                base_config = load_config(config_path)
            
            func_params = func(*args, **kwargs) or {}
            
            # Handle output pattern first
            final_output_pattern = output_pattern or base_config.get('output_pattern')
            if not final_output_pattern:
                raise ValueError("output_pattern must be provided either in config or decorator")
            
            # Build runtime options for extractor
            runtime_options = {
                'source_name': source_name or base_config.get('source_name'),
                'extractor_type': extractor_type or base_config.get('extractor_type'),
                'url_template': url_template or base_config.get('url_template'),
                **base_config.get('options', {}),
                **options,
                **kwargs
            }
            runtime_options = {k: v for k, v in runtime_options.items() if v is not None}
            
            # Generate parameters
            params = []
            if resources:
                resource_data = resources.get_resources()
                if resource_data.combination_type == "multiple":
                    params = [
                        {**{k.rstrip('s'): str(v) for k, v in zip(resource_data.data.keys(), values)},
                         **func_params}
                        for values in itertools.product(*resource_data.data.values())
                    ]
                else:  # direct combinations
                    params = [
                        {**item, **func_params}
                        for item in resource_data.data
                    ]
            else:
                params = [func_params] if func_params else [{}]

            # Filter existing files if needed
            filtered_params = []
            skipped_paths = []
            
            for param in params:
                if callable(final_output_pattern):
                    output_path = final_output_pattern(param)
                else:
                    output_path = Template(final_output_pattern).safe_substitute(**param)
                
                path_obj = Path(output_path).resolve()
                
                if skip_if_exists and path_obj.exists():
                    skipped_paths.append(str(path_obj))
                    continue
                    
                filtered_params.append(param)

            # Create and run extractor
            extractor = ExtractorFactory.create(**runtime_options)
            responses = extractor.extract_batch(filtered_params)

            # Save results
            results = []
            for param, response in zip(filtered_params, responses):
                if callable(final_output_pattern):
                    output_path = final_output_pattern(param)
                else:
                    output_path = Template(final_output_pattern).safe_substitute(**param)

                path_obj = Path(output_path).resolve()
                path_obj.parent.mkdir(parents=True, exist_ok=True)

                with open(path_obj, "w", encoding="utf-8") as f:
                    f.write(response)
                results.append(str(path_obj))
            if skipped_paths:
                logger.info(f"Total files skipped: {len(skipped_paths)}")
            return results + skipped_paths
            
        return wrapper
    return decorator


def resources(func: Callable[[], ResourceData]) -> ResourceProvider:
    return ResourceProvider(func)
