from typing import Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import BaseModel

ORMModel = TypeVar("ORMModel", bound=BaseModel)


class CRUDRepository(Generic[ORMModel]):

    def __init__(self, model: Type[ORMModel], db_session: Session) -> None:
        self.db_session = db_session
        self.model = model

    def create(self, **kwargs) -> ORMModel:
        """Creates a row in the database

        Args:
            self.db_session (Session): sqlalchemy Session

        Returns:
            ORMModel: The model instance of the created row
        """
        model_obj = self.model(**kwargs)
        self.db_session.add(model_obj)
        self.db_session.commit()
        self.db_session.refresh(model_obj)
        return model_obj

    def get_one(self, *args, **kwargs) -> ORMModel | None:
        """Gets model instances based on filters

        Args:
            self.db_session (Session): sqlalchemy Session
            *args: Filter expression such as Event.location_x > 0.5
            **kwargs: Equalility expresion such as name="david"

        Returns:
            list[ORMModel]: _description_
        """
        sql = select(self.model)

        # Condtional filter
        if args:
            sql = sql.where(*args)

        # Equalility filters
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                sql = sql.where(getattr(self.model, key) == value)

        result = self.db_session.execute(sql)

        return result.scalar_one_or_none()

    def get_all(self, *args, **kwargs) -> list[ORMModel]:
        """Gets model instances based on filters

        Args:
            self.db_session (Session): sqlalchemy Session
            *args: Filter expression such as Event.location_x > 0.5
            **kwargs: Equalility expresion such as name="david"

        Returns:
            list[ORMModel]: List of model instances
        """

        sql = select(self.model)

        # Condtional filter
        if args:
            sql = sql.where(*args)

        # Equalility filters
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                sql = sql.where(getattr(self.model, key) == value)

        result = self.db_session.execute(sql)

        return list(result.scalars().all())

    def delete(self, model_instance: ORMModel) -> ORMModel | None:
        """Deletes a model in the database

        Args:
            self.db_session (Session): Sqlalchemy Session
            model_instance (ORMModel): Instance of the model

        Returns:
            ORMModel | None: Returns none if model not found or not parsed
        """

        if model_instance:
            self.db_session.delete(model_instance)
            self.db_session.commit()
            return model_instance
        return None

    def update(self, model_instance: ORMModel, **update_data) -> ORMModel | None:
        """Updates a model instance

        Args:
            self.db_session (Session): sqlalchemy Session
            model_instance (ORMModel): Instance of the model

        Returns:
            ORMModel | None: Returns none if model not found or not parsed
        """
        if not model_instance:
            return None

        # Update the instance attributes
        for key, value in update_data.items():
            if hasattr(model_instance, key):
                setattr(model_instance, key, value)

        self.db_session.commit()
        self.db_session.refresh(model_instance)
        return model_instance
