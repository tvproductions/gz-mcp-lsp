"""Public synthetic subclass and member-override fixture."""


class Parent:
    def speak(self) -> str:
        return "parent"


class Child(Parent):
    def speak(self) -> str:
        return "child"


class Other(Parent):
    def speak(self) -> str:
        return "other"


class Unrelated:
    def speak(self) -> str:
        return "unrelated"
