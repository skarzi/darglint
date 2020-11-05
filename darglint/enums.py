import logging
from enum import Enum


class Strictness(Enum):
    """The minimum strictness with which to apply checks.

    Strictness does not describe whether or not a check
    should be applied. Rather, if a check is done, strictness
    describes how intense/strict/deep the check should be.

    Each level here describes what is required of the
    docstring at the given level of strictness.  For example,
    SHORT_DESCRIPTION describes the situation where one-liners are
    allowed, and sections are not required.

    If the docstring being checked contains more than the
    allowed amount below, then it is assumed that everything
    must be checked.

    """

    # Allow a single-line description.
    SHORT_DESCRIPTION = 1

    # Allow a single-line description followed by a long
    # description, but no sections.
    LONG_DESCRIPTION = 2

    # Require everything.
    FULL_DESCRIPTION = 3

    @classmethod
    def from_string(cls, strictness):
        strictness = strictness.lower().strip()
        if strictness in {'short_description', 'short'}:
            return cls.SHORT_DESCRIPTION
        if strictness in {'long_description', 'long'}:
            return cls.LONG_DESCRIPTION
        if strictness in {'full_description', 'full'}:
            return cls.FULL_DESCRIPTION

        raise Exception(
            'Unrecognized strictness amount "{}".  '.format(strictness) +
            'Should be one of {"short", "long", "full"}'
        )


class AssertStyle(Enum):
    """Describes how to handle assertions."""
    RAISE = 1
    LOG = 2


class LogLevel(Enum):
    """Describes the level of error which should be logged.

    These levels correspond to the levels in logging.
    This wrapper primarily serves as a means of conveniently
    parsing the levels, while maintaining the same interface
    as other options.

    """
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG

    @classmethod
    def from_string(cls, level):
        # type: (str) -> LogLevel
        normalized_level = level.lower().strip()
        if normalized_level == 'critical':
            return cls.CRITICAL
        elif normalized_level == 'error':
            return cls.ERROR
        elif normalized_level == 'warning':
            return cls.WARNING
        elif normalized_level == 'info':
            return cls.INFO
        elif normalized_level == 'debug':
            return cls.DEBUG
        else:
            raise ValueError('Unrecognized log level, "{}"'.format(
                level
            ))
