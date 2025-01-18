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
                "goal": user.goal
            }
        return None
