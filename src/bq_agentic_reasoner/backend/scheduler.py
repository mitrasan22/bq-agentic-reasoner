import threading
from typing import Callable


class AsyncScheduler:
    """
    Fire-and-forget async execution.
    Works locally and in Cloud Functions.
    """

    def run(self, fn: Callable, *args, **kwargs) -> None:
        thread = threading.Thread(
            target=fn,
            args=args,
            kwargs=kwargs,
            daemon=True,
        )
        thread.start()
