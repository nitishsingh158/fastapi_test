"""add foreign key to posts

Revision ID: 503c5b5421d0
Revises: 108728b33ac2
Create Date: 2024-06-11 22:30:24.159955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '503c5b5421d0'
down_revision: Union[str, None] = '108728b33ac2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("user_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
