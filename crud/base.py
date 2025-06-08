from typing import Type, TypeVar
from sqlalchemy.orm import Session

ORMModel = TypeVar("ORMModel")


class CRUDBase:

    def __init__(self, model: Type[ORMModel]):
        self.model = model

    def create(self, db: Session, **kwargs) -> ORMModel:
        model_obj = self.model(**kwargs)
        db.add(model_obj)
        db.commit()
        db.refresh(model_obj)
        return model_obj
