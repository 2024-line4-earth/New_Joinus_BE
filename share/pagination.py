# pagination.py
from rest_framework.pagination import CursorPagination

class SharedCardCursorPagination(CursorPagination):
    ordering = ("-created_at", "-id")
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
