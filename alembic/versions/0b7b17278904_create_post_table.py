"""create post table

Revision ID: 0b7b17278904
Revises: 
Create Date: 2024-06-11 22:04:51.203244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b7b17278904'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column(
                        "id",
                        sa.Integer(),
                        nullable = False,
                        primary_key = True),
                    sa.Column(
                        "title",
                        sa.String(),
                        nullable = False)
                    )


def downgrade() -> None:
    op.drop_table("posts")
