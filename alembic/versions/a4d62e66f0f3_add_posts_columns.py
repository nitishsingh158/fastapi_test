"""add posts columns

Revision ID: a4d62e66f0f3
Revises: 503c5b5421d0
Create Date: 2024-06-11 22:36:31.555181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4d62e66f0f3'
down_revision: Union[str, None] = '503c5b5421d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column(
                      "published",
                      sa.Boolean(),
                      nullable=False
                  ))
    op.add_column("posts", 
                  sa.Column(
                    "created_at",
                    sa.TIMESTAMP(timezone=True),
                    nullable=False, 
                    server_default=sa.text("NOW()")))
    pass    


def downgrade() -> None:
    op.drop_column("published", "created_at")
    pass
