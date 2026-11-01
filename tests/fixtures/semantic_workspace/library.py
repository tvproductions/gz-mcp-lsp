def mark[T](function: T) -> T:
    return function


@mark
def shared(
    name: str,
) -> str:
    """Synthetic reusable declaration."""
    return name.upper()


SHARED_CONSTANT = (
    "saved",
    "value",
)


class Outer:
    @staticmethod
    async def nested(
        item: str,
    ) -> str:
        return item.lower()
