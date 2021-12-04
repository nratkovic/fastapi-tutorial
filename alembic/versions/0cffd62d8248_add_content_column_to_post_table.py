"""add content column to post table

Revision ID: 0cffd62d8248
Revises: ceb4e55b6c78
Create Date: 2021-11-20 16:18:28.847856

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "0cffd62d8248"
down_revision = "ceb4e55b6c78"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
