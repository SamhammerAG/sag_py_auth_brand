from logging import Filter, LogRecord

from .request_brand_context import get_brand, get_brand_alias


class RequestBrandLoggingFilter(Filter):
    """Register this filter to get a field brand_name in log entries"""

    def __init__(self, name: str = "") -> None:
        super().__init__(name=name)

    def filter(self, record: LogRecord) -> bool:
        if request_brand := get_brand_alias() or get_brand():
            record.request_brand = request_brand

        return True
