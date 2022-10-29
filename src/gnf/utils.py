import json
import re
import time
from typing import Any
from typing import Optional

import pendulum
import property_format
from errors import SchemaError


DEFAULT_STEP_DURATION = 0.1

snake_add_underscore_to_camel_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name):
    return snake_add_underscore_to_camel_pattern.sub("_", name).lower()


def snake_to_camel(word):
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def dot_to_underscore(candidate: str) -> str:
    """Translation between two different formats for a list of alphanumeric
    words (where the most significant word does not start with a number).

    Args:
        candidate (str): left-right-dot format. Most significant word on the
        left, word seperators are periods.

    Raises:
        SchemaError: if input is not left-right-dot format

    Returns:
        str:  Same string in LRU format. Seperator is now underscore, most
        significant word still on the left.
    """
    try:
        property_format.check_is_lrd_alias_format(candidate)
    except SchemaError:
        raise SchemaError(
            f"{candidate} words with dot as separator are not alphanumeric!"
        )

    return candidate.replace(".", "_")


def underscore_to_dot(candidate: str) -> str:
    """Replaces underscores to dots in a string, checking that all words between
    seperators are alphanumeric.
    """
    if property_format.is_lru_alias_format(candidate):
        return candidate.replace("_", ".")
    else:
        raise SchemaError(
            f"{candidate} words with underscore as separator are not alphanumeric!"
        )


def responsive_sleep(
    obj,
    seconds: float,
    step_duration: float = DEFAULT_STEP_DURATION,
    running_field_name: str = "_main_loop_running",
) -> bool:
    """Sleep in way that is more responsive to thread termination: sleep in step_duration increments up to
    specificed seconds, at after each step checking self._main_loop_running"""
    sleeps = int(seconds / step_duration)
    if sleeps * step_duration != seconds:
        last_sleep = seconds - (sleeps * step_duration)
    else:
        last_sleep = 0
    for _ in range(sleeps):
        if getattr(obj, running_field_name):
            time.sleep(step_duration)
    if getattr(obj, running_field_name) and last_sleep > 0:
        time.sleep(last_sleep)
    return getattr(obj, running_field_name)


class StreamlinedSerializerMixin:
    @property
    def streamlined_serialize(self):
        output = {}
        for key, value in self.__dict__.items():
            if value is not None:
                output[key] = value

        return json.dumps(output)


class MessageSummary:
    """Helper class for formating message summaries message receipt/publication single line summaries."""

    DEFAULT_FORMAT = (
        "{timestamp}  {direction:4s}  {actor_alias:33s}  {broker_flag}  {arrow:2s}  {topic:80s}"
        "  {payload_type}"
    )

    @classmethod
    def format(
        cls,
        direction: str,
        actor_alias: str,
        topic: str,
        payload_object: Any = None,
        broker_flag=" ",
        timestamp: Optional[pendulum.datetime] = None,
    ) -> str:
        """
        Formats a single line summary of message receipt/publication.

        Args:
            direction: "IN" or "OUT"
            actor_alias: The node alias of the sending or receiving actor.
            topic: The destination or source topic.
            payload_object: The payload of the message.
            broker_flag: "*" for the "gw" broker.
            timestamp: "pendulum.now("UTC") by default.

        Returns:
            Formatted string.
        """
        try:
            if timestamp is None:
                timestamp = pendulum.now("UTC")
            direction = direction[:3].strip().upper()
            if direction in ["OUT", "SND"]:
                arrow = "->"
            elif direction.startswith("IN") or direction.startswith("RCV"):
                arrow = "<-"
            else:
                arrow = "? "
            if hasattr(payload_object, "__class__"):
                payload_str = payload_object.__class__.__name__
            else:
                payload_str = type(payload_object)
            return cls.DEFAULT_FORMAT.format(
                timestamp=timestamp.isoformat(),
                direction=direction,
                actor_alias=actor_alias,
                broker_flag=broker_flag,
                arrow=arrow,
                topic=f"[{topic}]",
                payload_type=payload_str,
            )
        except Exception as e:
            print(f"ouch got {e}")
            return ""