from pydantic import BaseModel


class PaginationMetadata(BaseModel):
    """
    Pagination metadata.
    """

    page: int
    page_size: int
    total_records: int
    total_pages: int
