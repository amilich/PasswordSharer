from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
service_membership = Table('service_membership', post_meta,
    Column('servicemembership_id', Integer, primary_key=True, nullable=False),
    Column('service_id', Integer),
    Column('group_id', Integer),
)

service = Table('service', pre_meta,
    Column('service_id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=120)),
    Column('password', VARCHAR(length=64)),
    Column('owner', VARCHAR(length=120)),
    Column('group_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['service_membership'].create()
    pre_meta.tables['service'].columns['group_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['service_membership'].drop()
    pre_meta.tables['service'].columns['group_id'].create()
