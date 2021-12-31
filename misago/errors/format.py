from typing import Sequence, Union, cast

from .autherror import AuthError
from .errordict import ErrorDict

ROOT_LOCATION = "__root__"


def get_error_dict(
    error: Exception, location: Union[str, Sequence[str]] = ROOT_LOCATION
) -> ErrorDict:
    if not isinstance(location, (list, tuple)):
        location = (cast(str, location),)

    return {
        "loc": tuple(location),
        "type": get_error_type(error),
        "msg": str(error),
    }


def get_error_type(error: Exception) -> str:
    if isinstance(error, AssertionError):
        return "assertion_error"

    base_name = "value_error"
    if isinstance(error, TypeError):
        base_name = "type_error"
    if isinstance(error, AuthError):
        base_name = "auth_error"

    code = (
        getattr(error, "code", None)
        or type(error).__name__.replace("Error", "").lower()
    )
    return base_name + "." + code
