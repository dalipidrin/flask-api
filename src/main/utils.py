from sqlalchemy import inspect


def to_dict(entity):
    """
    Convert SQLAlchemy model instance to dict excluding internal attributes.
    """
    return {c.key: getattr(entity, c.key) for c in inspect(entity).mapper.column_attrs}
