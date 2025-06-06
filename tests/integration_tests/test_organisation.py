from database.enums.country_codes import CountryCode
from database.models.organisation import Organisation


def test_create_organisation_row(sample_organisation_object, test_db_session):
    test_db_session.add(sample_organisation_object)
    test_db_session.flush()
    
    assert sample_organisation_object.id is not None

    found_org = test_db_session.query(Organisation).filter_by(name="Test Org").first()
    assert found_org is not None
    assert found_org.name == "Test Org"
    assert found_org.country_code == CountryCode.GB
    