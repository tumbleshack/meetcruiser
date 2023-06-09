from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column

class TimestampMixin(object):
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime, nullable=True)