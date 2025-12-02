from database import new_session, TaskTable
from schemas import STaskAdd, STask
from sqlalchemy import select


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int: 
        async with new_session() as session:
            task_dict = data.model_dump() # приводит к словарю
            task = TaskTable(**task_dict)
            session.add(task)
            await session.flush() # не завершит транзакцию, но отправит изменения в бвзу, чтобы получить id 
            await session.commit()
            return task.id
        

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskTable)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task) for task in task_models] # преобразование моделей бд в схемы
            return task_schemas



