from typing import Any


class VoterCreationFailureException(Exception):
    def __init__(self, reason: str, *args: Any, **kwargs: Any) -> None:
        self.reason = reason
        super().__init__(*args, **kwargs)
