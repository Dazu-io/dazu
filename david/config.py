import copy
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple

from david.util import json_to_string


class InvalidConfigError(ValueError):
    """Raised if an invalid configuration is encountered."""

    def __init__(self, message: Text) -> None:
        super().__init__(message)


def component_config_from_pipeline(
    index: int,
    pipeline: List[Dict[Text, Any]],
    defaults: Optional[Dict[Text, Any]] = None,
) -> Dict[Text, Any]:
    try:
        c = pipeline[index]
        return override_defaults(defaults, c)
    except IndexError:
        warnings.warn(
            f"Tried to get configuration value for component "
            f"number {index} which is not part of the pipeline. "
            f"Returning `defaults`."
        )
        return override_defaults(defaults, {})


# Config class inspired by RasaHQ/rasa
def override_defaults(
    defaults: Optional[Dict[Text, Any]], custom: Optional[Dict[Text, Any]]
) -> Dict[Text, Any]:
    if defaults:
        cfg = copy.deepcopy(defaults)
    else:
        cfg = {}

    if custom:
        cfg.update(custom)
    return cfg


class DavidConfig:
    def __init__(self, configuration_values: Optional[Dict[Text, Any]] = None) -> None:
        """Create a model configuration, optionally overriding
        defaults with a dictionary ``configuration_values``.
        """
        if not configuration_values:
            configuration_values = {}

        self.language = "en"
        self.pipeline = []
        self.data = None

        self.override(configuration_values)

        if self.__dict__["pipeline"] is None:
            # replaces None with empty list
            self.__dict__["pipeline"] = []
        # elif isinstance(self.__dict__["pipeline"], str):
        # from rasa.nlu import registry

        # template_name = self.__dict__["pipeline"]

        # pipeline = registry.pipeline_template(template_name)

        # if pipeline:
        #     # replaces the template with the actual components
        #     self.__dict__["pipeline"] = pipeline
        # else:
        #     known_templates = ", ".join(
        #         registry.registered_pipeline_templates.keys()
        #     )

        #     raise InvalidConfigError(
        #         f"No pipeline specified and unknown "
        #         f"pipeline template '{template_name}' passed. Known "
        #         f"pipeline templates: {known_templates}"
        #     )

        for key, value in self.items():
            setattr(self, key, value)

    def __getitem__(self, key: Text) -> Any:
        return self.__dict__[key]

    def get(self, key: Text, default: Any = None) -> Any:
        return self.__dict__.get(key, default)

    def __setitem__(self, key: Text, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: Text) -> None:
        del self.__dict__[key]

    def __contains__(self, key: Text) -> bool:
        return key in self.__dict__

    def __len__(self) -> int:
        return len(self.__dict__)

    def __getstate__(self) -> Dict[Text, Any]:
        return self.as_dict()

    def __setstate__(self, state: Dict[Text, Any]) -> None:
        self.override(state)

    def items(self) -> List[Any]:
        return list(self.__dict__.items())

    def as_dict(self) -> Dict[Text, Any]:
        return dict(list(self.items()))

    def view(self) -> Text:
        return json_to_string(self.__dict__, indent=4)

    def for_component(self, index, defaults=None) -> Dict[Text, Any]:
        return component_config_from_pipeline(index, self.pipeline, defaults)

    @property
    def component_names(self) -> List[Text]:
        if self.pipeline:
            return [c.get("name") for c in self.pipeline]
        else:
            return []

    def set_component_attr(self, index, **kwargs) -> None:
        try:
            self.pipeline[index].update(kwargs)
        except IndexError:
            warnings.warn(
                f"Tried to set configuration value for component "
                f"number {index} which is not part of the pipeline."
            )

    def override(self, config) -> None:
        if config:
            self.__dict__.update(config)
