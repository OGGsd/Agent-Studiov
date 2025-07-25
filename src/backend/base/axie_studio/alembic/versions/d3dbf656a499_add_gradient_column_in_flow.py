"""add gradient column in Flow

Revision ID: d3dbf656a499
Revises: e5a65ecff2cd
Create Date: 2024-09-27 09:35:19.424089

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.engine.reflection import Inspector

from axie_studio.utils import migration

# revision identifiers, used by Alembic.
revision: str = 'd3dbf656a499'
down_revision: Union[str, None] = 'e5a65ecff2cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flow', schema=None) as batch_op:
        if not migration.column_exists(table_name='flow', column_name='gradient', conn=conn):
            batch_op.add_column(sa.Column('gradient', sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flow', schema=None) as batch_op:
        if migration.column_exists(table_name='flow', column_name='gradient', conn=conn):
            batch_op.drop_column('gradient')

    # ### end Alembic commands ###
