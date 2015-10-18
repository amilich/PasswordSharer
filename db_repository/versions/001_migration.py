from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
group = Table('group', post_meta,
    Column('group_id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('group_hash', String(length=5)),
)

group_membership = Table('group_membership', post_meta,
    Column('membership_id', Integer, primary_key=True, nullable=False),
    Column('groupid', Integer),
    Column('user_id', Integer),
)

service = Table('service', post_meta,
    Column('service_id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('password', String(length=64)),
    Column('owner', String(length=120)),
    Column('group_id', Integer),
)

user = Table('user', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['group'].create()
    post_meta.tables['group_membership'].create()
    post_meta.tables['service'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['group'].drop()
    post_meta.tables['group_membership'].drop()
    post_meta.tables['service'].drop()
    post_meta.tables['user'].drop()
