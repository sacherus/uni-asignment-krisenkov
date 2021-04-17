import json
import os
import re
import sys
from functools import wraps
import logging

logger = logging.getLogger(__name__)

WARN_ON_MISSING = True

NO_ARGUMENT = object()

TRUE_CHOICES = {"on", "enabled", "yes", "true", "1"}


class MissingValueError(ValueError):
    pass


def handle_errors(f):
    @wraps(f)
    def _wrapper(name, *args, exit=True, **kwargs):
        try:
            return f(name, *args, **kwargs)
        except MissingValueError:
            if WARN_ON_MISSING:
                logger.warning(
                    "Variable {key} was expected and is missing".format(key=name)
                )
                return None
            else:
                logger.error("Variable {key} is missing".format(key=name))

                if exit:
                    sys.exit(1)
                else:
                    raise

        except ValueError as e:
            logger.error(
                "Configuration error for key {key}: {message}".format(
                    key=name, message=str(e)
                )
            )
            if exit:
                sys.exit(1)
            else:
                raise

    return _wrapper


@handle_errors
def read(name, default=NO_ARGUMENT):
    if name not in os.environ:
        if default is NO_ARGUMENT:
            raise MissingValueError
        else:
            return default
    return os.environ[name]


@handle_errors
def read_boolean(name, default=NO_ARGUMENT):
    if name not in os.environ:
        if default is NO_ARGUMENT:
            raise MissingValueError
        else:
            return default
    return os.environ[name].strip().lower() in TRUE_CHOICES


@handle_errors
def read_int(name, default=NO_ARGUMENT):
    value = os.environ.get(name)
    if value is None:
        if default is NO_ARGUMENT:
            raise MissingValueError
        else:
            return default
    else:
        if not re.match("^\d+$", value):
            raise ValueError("Only digits are allowed for this value".format(name=name))
        return int(value)


@handle_errors
def read_list(name, default=NO_ARGUMENT, separator=","):
    """Anything like VAR=1, 2, 3 will be converted to ['1', '2', '3']"""
    value = os.environ.get(name)
    if value is None:
        if default is NO_ARGUMENT:
            return []
        else:
            return default
    return [v.strip() for v in value.split(separator) if v.strip()]


@handle_errors
def read_json(name, default=NO_ARGUMENT):
    """Expect json string on input"""
    value = os.environ.get(name)
    if value is None:
        if default is NO_ARGUMENT:
            return None
        else:
            return default
    try:
        value_json = json.loads(value)
    except:
        raise ValueError(f"String `{value}` cannot be parsed as json")
    return value_json
