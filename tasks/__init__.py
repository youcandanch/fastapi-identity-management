import sys

from invoke import task

RUN_DEFAULTS = {
    "echo": True,
    "pty": sys.stdout.isatty(),
}


@task
def lint(ctx):
    ctx.run("black .", **RUN_DEFAULTS)
    ctx.run("isort .", **RUN_DEFAULTS)
    ctx.run("pylint identity_service/", **RUN_DEFAULTS)


@task
def run(ctx):
    ctx.run("uvicorn identity_service.main:app --reload", **RUN_DEFAULTS)
