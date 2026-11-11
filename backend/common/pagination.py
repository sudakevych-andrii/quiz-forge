from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    """?page=2&page_size=50 -> {"count", "page", "page_size", "total_pages", "results"}."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: Any) -> Response:
        assert self.page is not None
        return Response(
            {
                "count": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """OpenAPI description of the response above (used by drf-spectacular)."""
        return {
            "type": "object",
            "required": ["count", "page", "page_size", "total_pages", "results"],
            "properties": {
                "count": {"type": "integer", "example": 42},
                "page": {"type": "integer", "example": 1},
                "page_size": {"type": "integer", "example": 20},
                "total_pages": {"type": "integer", "example": 3},
                "results": schema,
            },
        }
