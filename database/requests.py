from database.models import async_session
from database.models import User, BottomPFC, BottomDiet, BottomTraining
from sqlalchemy import select


from sqlalchemy.future import select
from database.models import User, async_session


async def set_user(
    tg_id: int,
    name: str,
    sex: str,
    age: int,
    height: int,
    weight: int,
    ph_condition: str,
    ch_illnesses: str,
    goal: str,
    is_registered: bool,
) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(
                tg_id=tg_id,
                name=name,
                sex=sex,
                age=age,
                height=height,
                weight=weight,
                ph_condition=ph_condition,
                ch_illnesses=ch_illnesses,
                goal=goal,
                is_registered=is_registered,
            )
            session.add(user)
            await session.commit()
        else:
            user.name = name
            user.sex = sex
            user.age = age
            user.height = height
            user.weight = weight
            user.ph_condition = ph_condition
            user.ch_illnesses = ch_illnesses
            user.goal = goal
            user.is_registered = is_registered
            await session.commit()

        return user


async def get_user_data(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalars().first()
        if user:
            return {
                "name": user.name,
                "sex": user.sex,
                "age": user.age,
                "height": user.height,
                "weight": user.weight,
                "ph_condition": user.ph_condition,
                "ch_illnesses": user.ch_illnesses,
                "goal": user.goal,
            }
        return None


async def bju_request(tg_id: int, request: str):
    async with async_session() as session:
        new_request = BottomPFC(tg_id=tg_id, request=request)
        session.add(new_request)
        await session.commit()


async def diet_plan_request(tg_id: int):
    async with async_session() as session:
        new_request = BottomDiet(tg_id=tg_id, request=True)
        session.add(new_request)
        await session.commit()


async def training_plan_request(tg_id: int):
    async with async_session() as session:
        new_request = BottomTraining(tg_id=tg_id, request=True)
        session.add(new_request)
        await session.commit()
