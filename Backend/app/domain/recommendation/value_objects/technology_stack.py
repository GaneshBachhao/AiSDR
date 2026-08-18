from dataclasses import dataclass


@dataclass(frozen=True)
class TechnologyStack:
    """
    Represents a technology used in a proposed solution.
    """

    name: str

    version: str | None = None

    vendor: str | None = None

    remarks: str | None = None

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if not self.name.strip():
            raise ValueError("Technology name cannot be empty.")

        if self.version is not None and not self.version.strip():
            raise ValueError("Version cannot be empty.")

        if self.vendor is not None and not self.vendor.strip():
            raise ValueError("Vendor cannot be empty.")

        if self.remarks is not None and not self.remarks.strip():
            raise ValueError("Remarks cannot be empty.")
