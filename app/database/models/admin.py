from ormar import Model, Integer, Float, IndexColumns
from database.connection import BaseMeta


class Admin(Model):
    class Meta(BaseMeta):
        tablename = "admins"
        constraints = [IndexColumns('chat_id', postgresql_using='btree')]

    id: int = Integer(primary_key=True)
    chat_id: int = Integer(nullable=False)
    debt: float = Float(nullable=False, default=0)
