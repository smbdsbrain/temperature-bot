from invoke import task


@task(default=True)
def start_bot(ctx):
    from bot.bot import run
    run(ctx.config)
