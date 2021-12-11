"""add is_active column in users table

Revision ID: cab9c5d6a8ad
Revises: 682c49381583
Create Date: 2021-12-07 19:04:02.291082

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "cab9c5d6a8ad"
down_revision = "682c49381583"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), server_default="True", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###