from functools import total_ordering


@total_ordering
class VersionNumber:
    """
    Immutable semantic version number.
    """

    def __init__(
        self,
        major: int,
        minor: int = 0,
    ):
        if major < 0:
            raise ValueError("Major version cannot be negative.")

        if minor < 0:
            raise ValueError("Minor version cannot be negative.")

        self._major = major
        self._minor = minor

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    def next_major(self):
        return VersionNumber(
            self.major + 1,
            0,
        )

    def next_minor(self):
        return VersionNumber(
            self.major,
            self.minor + 1,
        )

    def __eq__(self, other):
        return isinstance(other, VersionNumber) and (
            self.major,
            self.minor,
        ) == (
            other.major,
            other.minor,
        )

    def __lt__(self, other):
        if not isinstance(other, VersionNumber):
            return NotImplemented

        return (
            self.major,
            self.minor,
        ) < (
            other.major,
            other.minor,
        )

    def __hash__(self):
        return hash(
            (
                self.major,
                self.minor,
            )
        )

    def __str__(self):
        return f"{self.major}.{self.minor}"
