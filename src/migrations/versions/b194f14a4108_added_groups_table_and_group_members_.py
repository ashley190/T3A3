"""Added groups table and group_members linking table

Revision ID: b194f14a4108
Revises: e9ac5ea6b1c7
Create Date: 2020-12-14 22:36:12.039241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b194f14a4108'
down_revision = 'e9ac5ea6b1c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_table('group_members',
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.profile_id'], ),
    sa.PrimaryKeyConstraint('profile_id', 'group_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_members')
    op.drop_table('groups')
    # ### end Alembic commands ###
