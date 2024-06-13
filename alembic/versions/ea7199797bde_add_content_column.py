"""add content column

Revision ID: ea7199797bde
Revises: 0b7b17278904
Create Date: 2024-06-11 22:16:45.489620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea7199797bde'
down_revision: Union[str, None] = '0b7b17278904'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column(
                      "content",
                      sa.String(),
                      nullable=False
                  ))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
