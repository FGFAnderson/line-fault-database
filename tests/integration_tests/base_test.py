from typing import Type
from sqlalchemy import Column, inspect, Enum
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from database.models import Organisation
from datetime import datetime
import pytest


# This class is used to autogenerate mock data for any ORM model which inherits DeclaritiveBase
class ORMTestDataGenerator[T: DeclarativeBase]:
    def __init__(self, model: Type[T]):
        self.model = model
        self.model_inspector = inspect(model)

    def generate_valid_args_for_model(self):
        # Create a copy of the model's columns
        columns = list(self.model_inspector.columns)
        # Remove the primary key from the list as that's autoincremented so doesn't need to be set, look into advancing this later to handle compound keys
        columns.remove(self.model_inspector.primary_key[0])

        model_kwargs = {}

        for col in columns:
            model_kwargs[col.name] = self._get_valid_data_for_column(col)

        return model_kwargs

    def _get_valid_data_for_column(self, column: sqlalchemy.Column):
        """Generates valid data for any column based on it's type

        Args:
            column (Column):

        Returns:
            Union[str, int, float, datetime, boolean]: A valid value for the column's data type.
        """

        if isinstance(column.type, sqlalchemy.Enum):
            return column.type.enums[0]

        if isinstance(column.type, sqlalchemy.CHAR):
            length = getattr(column.type, "length", 1)
            value = f"test_{column.name}"
            return value.ljust(length)[:length]

        elif isinstance(column.type, sqlalchemy.VARCHAR):
            max_length = getattr(column.type, "length", 50)
            return f"test_string_{column.name}"[:max_length]

        elif isinstance(column.type, sqlalchemy.String):
            max_length = getattr(column.type, "length", 50)
            return f"test_string_{column.name}"[:max_length]

        elif isinstance(column.type, sqlalchemy.Integer):
            return 42

        elif isinstance(column.type, sqlalchemy.Float):
            return 42.0

        elif isinstance(column.type, sqlalchemy.Boolean):
            return True

        elif isinstance(column.type, sqlalchemy.DateTime):
            return datetime.now()


class BaseORMModelTests:

    model_class = None

    @pytest.fixture(autouse=True)
    def setup_base_orm_tests(self):
        """Setup method that runs before each test."""
        if self.model_class is None:
            raise ValueError("model_class must be set in the inheriting test class")

        self.model = self.model_class
        self.data_generator = ORMTestDataGenerator(self.model)
        self.inspector = inspect(self.model)

    def test_create_model_in_db(self, test_db_session):
        """Test creating a model in the database."""
        model_data = self.data_generator.generate_valid_args_for_model()
        model_obj = self.model(**model_data)

        test_db_session.add(model_obj)
        test_db_session.flush()

        assert model_obj is not None

        pk_column = self.inspector.primary_key[0]
        pk_value = getattr(model_obj, pk_column.name)

        created_model = (
            test_db_session.query(self.model_class)
            .filter(pk_column == pk_value)
            .first()
        )

        assert created_model is not None
        for key, expected_value in model_data.items():
            actual_value = getattr(created_model, key)
            assert actual_value == expected_value


class TestOrganisation(BaseORMModelTests):

    model_class = Organisation


# For enums we can make a function something like 'get valid enun' which could use a function to get the enum from the Column type
# Then we need to provide an invalid enum, we can do this but looking at the type of the enum and creating an string not in the enum list
# Or we could see how enums work in python and try and declare something like Enum.{random_string}
# Then we use the valid enum for constructing a valid data type to be used in the creation of the type and after that we can test against it

# For creating strings we can look to see if it's a str type then look at it's length property and slice a test string if needed
# For integers we can use a predfined int
# For dates we can just use func.now
# For floats we can just use a predefined float
# For unique we can test against unique

# Later on we can use at constraints and try and test those

# for col in columns:
#    print(col.type.length)


# Step 1: For every column which is not a PK and is not a function value Create Read Update and Delete it to test crud

# If the column is not the PK or has a default value add it to the list of ediatble columns
# Check the columns type and insert valid test data into the column
# Then test against CRUD operations

# For every column with a constraint we can try and test against the constraint

# If it's the primary key during the create we don't have to use it
# We can also not use the optitionals and test against them, interesting things is to look for constraints and challenge them for the automatic test
