from typing import Any, Dict

Settings = Dict[str, Any]


class DynamicSettings(Settings):
    _overrides: Settings = {}

    def __getitem__(self, setting: str) -> Any:
        if setting in self._overrides:
            return self._overrides[setting]
        try:
            return super().__getitem__(setting)
        except KeyError as exception:
            raise KeyError(f"Setting '{setting}' is not defined.") from exception

    @classmethod
    def override_settings(cls, overrides: Settings):
        cls._overrides = overrides

    @classmethod
    def remove_overrides(cls):
        cls._overrides = {}
