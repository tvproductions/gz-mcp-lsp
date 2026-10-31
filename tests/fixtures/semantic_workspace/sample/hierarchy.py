class Service:
    def run(self) -> str:
        return "base"


class CustomService(Service):
    def run(self) -> str:
        return "custom"


def outer():
    def inner() -> str:
        return "nested"

    return inner()
