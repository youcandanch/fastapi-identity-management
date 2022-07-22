import asyncio
from logging.config import fileConfig

from alembic import context
from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from identity_service..models import User

config = context.config
fileConfig(config.config_file_name)
target_metadata = SQLModel.metadata


def process_revision_directives(context, revision, directives):
    """
    In order to get sequential migrations similar to the Django formatting -- like
    0001_name, 0002_name, etc. -- we're putting in some custom logic for the
    `process_revision_directives` parameter of configuring Alembic context. See
    https://alembic.sqlalchemy.org/en/latest/api/runtime.html for more details.
    """
    migration_script = directives[0]
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()
    if head_revision is None:
        new_rev_id = 1
    else:
        last_rev_id = int(head_revision.lstrip("0"))
        new_rev_id = last_rev_id + 1
    migration_script.rev_id = "{0:04}".format(new_rev_id)


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        process_revision_directives=process_revision_directives,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


asyncio.run(run_migrations_online())
