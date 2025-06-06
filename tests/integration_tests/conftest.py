import pytest
from database.db import create_schema, session_maker

@pytest.fixture(scope="function")
def test_db_session():
    """Test version that never commits."""
    session = session_maker()
    transaction = session.begin()
    try:
        yield session
    except Exception:
        transaction.rollback()
        raise
    finally:
        transaction.rollback() 
        session.close()
        
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_schema()
