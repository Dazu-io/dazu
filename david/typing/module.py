from abc import ABCMeta


class Module:
    """Metaclass with `name` class property"""

    @classmethod
    def name(cls):
        """The name property is a function of the class - its __name__."""

        return cls.__name__
