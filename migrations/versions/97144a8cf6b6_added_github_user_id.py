# SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
#
# SPDX-License-Identifier: MPL-2.0

"""Added github_user_id

Revision ID: 97144a8cf6b6
Revises: b2acaede5c2f
Create Date: 2022-12-17 16:25:44.446361

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = "97144a8cf6b6"
down_revision = "b2acaede5c2f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("github_user_id", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "github_user_id")
    # ### end Alembic commands ###
