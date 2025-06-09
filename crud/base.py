from typing import Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import BaseModel


class CRUDBase:

    def __init__(self, model: Type[BaseModel]) -> None:
        self.model = model

    def create(self, db: Session, **kwargs) -> BaseModel:
        """Creates a row in the database

        Args:
            db (Session): sqlalchemy Session

        Returns:
            BaseModel: The model instance of the created row
        """
        model_obj = self.model(**kwargs)
        db.add(model_obj)
        db.commit()
        db.refresh(model_obj)
        return model_obj

    def get_one(self, db: Session, *args, **kwargs) -> BaseModel | None:
        """Gets model instances based on filters

        Args:
            db (Session): sqlalchemy Session
            *args: Filter expression such as Event.location_x > 0.5
            **kwargs: Equalility expresion such as name="david"

        Returns:
            list[BaseModel]: _description_
        """
        sql = select(self.model)

        # Condtional filter
        if args:
            sql = sql.where(*args)

        # Equalility filters
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                sql = sql.where(getattr(self.model, key) == value)

        result = db.execute(sql)

        return result.scalar_one_or_none()

    def get_all(self, db: Session, *args, **kwargs) -> list[BaseModel]:
        """Gets model instances based on filters

        Args:
            db (Session): sqlalchemy Session
            *args: Filter expression such as Event.location_x > 0.5
            **kwargs: Equalility expresion such as name="david"

        Returns:
            list[BaseModel]: List of model instances
        """

        sql = select(self.model)

        # Condtional filter
        if args:
            sql = sql.where(*args)

        # Equalility filters
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                sql = sql.where(getattr(self.model, key) == value)

        result = db.execute(sql)

        return list(result.scalars().all())

    def delete(self, db: Session, model_instance: BaseModel) -> BaseModel | None:
        """Deletes a model in the database

        Args:
            db (Session): Sqlalchemy Session
            model_instance (BaseModel): Instance of the model

        Returns:
            BaseModel | None: Returns none if model not found or not parsed
        """

        if model_instance:
            db.delete(model_instance)
            db.commit()
            return model_instance
        return None

    def update(
        self, db: Session, model_instance: BaseModel, **update_data
    ) -> BaseModel | None:
        """Updates a model instance

        Args:
            db (Session): sqlalchemy Session
            model_instance (BaseModel): Instance of the model

        Returns:
            BaseModel | None: Returns none if model not found or not parsed
        """
        if not model_instance:
            return None

        # Update the instance attributes
        for key, value in update_data.items():
            if hasattr(model_instance, key):
                setattr(model_instance, key, value)

        db.commit()
        db.refresh(model_instance)
        return model_instance
