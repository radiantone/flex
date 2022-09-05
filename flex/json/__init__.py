import copy
import dataclasses
import json
import re


class DataclassEncoder(json.JSONEncoder):
    is_special = re.compile(r"^__[^\d\W]\w*__\Z", re.UNICODE)  # Dunder name.

    def default(self, obj):
        return self._asdict(obj)

    def _asdict(self, obj, *, dict_factory=dict):
        if not dataclasses.is_dataclass(obj):
            raise TypeError("_asdict() should only be called on dataclass instances")
        return self._asdict_inner(obj, dict_factory)

    def _asdict_inner(self, obj, dict_factory):
        if dataclasses.is_dataclass(obj):
            result = []
            # Get values of its fields (recursively).
            for f in dataclasses.fields(obj):
                value = self._asdict_inner(getattr(obj, f.name), dict_factory)
                result.append((f.name, value))
            # Add values of non-special attributes which are properties.
            is_special = self.is_special.match  # Local var to speed access.
            for name, attr in vars(type(obj)).items():
                if not is_special(name) and isinstance(attr, property):
                    result.append((name, attr.__get__(obj)))  # Get property's value.
            return dict_factory(result)
        elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
            return type(obj)(*[self._asdict_inner(v, dict_factory) for v in obj])
        elif isinstance(obj, (list, tuple)):
            return type(obj)(self._asdict_inner(v, dict_factory) for v in obj)
        elif isinstance(obj, dict):
            return type(obj)(
                (
                    self._asdict_inner(k, dict_factory),
                    self._asdict_inner(v, dict_factory),
                )
                for k, v in obj.items()
            )
        else:
            return copy.deepcopy(obj)
