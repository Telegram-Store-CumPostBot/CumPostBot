from database.engine import engine, Base

# from database.models.tables.admin import Admin
# from database.models.tables.tg_bot import TGBot
# from database.models.tables.customer import Customer
# from database.models.tables. import
# from database.models.tables. import
# from database.models.tables. import


async def init_models(drop=False):
    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def connect_to_database(drop=False):
    while True:
        try:
            await init_models(drop)
            break
        except ZeroDivisionError:
            print('find error')
            continue
