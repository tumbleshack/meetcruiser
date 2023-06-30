from sqlalchemy import DateTime, func, Enum
from sqlalchemy.orm import mapped_column
from marshmallow_sqlalchemy import ModelConverter, SQLAlchemyAutoSchema
from marshmallow import fields


class TimestampMixin(object):
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime, nullable=True)


class EnumField(fields.Field):
    def __init__(self, *args, **kwargs):
        self.column = kwargs.get("column")
        super(EnumField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj):
        field = super(EnumField, self)._serialize(value, attr, obj)
        try:
            return field.value if field else field
        except AttributeError:
            return field

    def deserialize(self, value, attr=None, data=None):
        field = super(EnumField, self).deserialize(value, attr, data)
        if isinstance(field, str) and self.column is not None:
            return self.column.type.python_type(field)
        return field


class ExtendModelConverter(ModelConverter):
    SQLA_TYPE_MAPPING = {
        **ModelConverter.SQLA_TYPE_MAPPING,
        Enum: EnumField,
    }

    def _add_column_kwargs(self, kwargs, column):
        super()._add_column_kwargs(kwargs, column)
        if hasattr(column.type, "enums"):
            kwargs["column"] = column
