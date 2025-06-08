from crud.base import CRUDBase
from database.db import get_db_session
from database.enums.country_codes import CountryCode
from database.models.organisation import Organisation


def test_create_organisation():
    crud_obj = CRUDBase(Organisation)

    try:
        with get_db_session() as session:
            new_org = crud_obj.create(
                session,
                name="Test Organisation",
                country_code=CountryCode.GB,
                region="South",
                website="https://test.com",
                logo_url="https://test.com/logo.png",
            )
            print(f"Created organisation: {new_org}")
            session.refresh(new_org)
    except Exception as e:
        print(f"Error creating organisation: {e}")


print(test_create_organisation())
