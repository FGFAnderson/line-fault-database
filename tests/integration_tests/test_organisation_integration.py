import pytest
from sqlalchemy.exc import IntegrityError, DataError
from database.enums.country_codes import CountryCode
from database.models.organisation import Organisation


def test_create_organisation_in_db(sample_organisation_object, test_db_session):
    """Tests creating an organisation in the database"""
    test_db_session.add(sample_organisation_object)
    test_db_session.flush()

    assert sample_organisation_object.id is not None

    created_org = (
        test_db_session.query(Organisation)
        .filter_by(name=sample_organisation_object.name)
        .first()
    )

    assert created_org is not None
    assert created_org.name == sample_organisation_object.name
    assert created_org.country_code == sample_organisation_object.country_code
    assert created_org.website == sample_organisation_object.website
    assert created_org.logo_url == sample_organisation_object.logo_url


def test_organisation_country_code_enum_constraint(test_db_session):
    """Tests creating an organisation with an invalid country code"""
    org = Organisation(name="Test Org", country_code="INVALID")
    with pytest.raises(DataError, match="invalid input value for enum countrycode"):
        test_db_session.add(org)
        test_db_session.flush()


def test_create_organisation_in_db_with_no_name(test_db_session):
    """Tests creating an organisation with name field as None"""
    org = Organisation(name=None, country_code=CountryCode.GB)
    with pytest.raises(IntegrityError, match='null value in column "name"'):
        test_db_session.add(org)
        test_db_session.flush()


def test_create_organisation_in_db_with_no_country_code(test_db_session):
    """Tests creating of organisation with country_code as None"""
    org = Organisation(name="Test Org", country_code=None)
    with pytest.raises(IntegrityError, match='null value in column "country_code"'):
        test_db_session.add(org)
        test_db_session.flush()


def test_organisation_unique_name_constraint(test_db_session):
    """Tests name of an organisation is unique"""
    org1 = Organisation(name="test", country_code=CountryCode.US)
    org2 = Organisation(name="test", country_code=CountryCode.GB)

    test_db_session.add(org1)
    test_db_session.flush()

    test_db_session.add(org2)
    with pytest.raises(
        IntegrityError, match="duplicate key value violates unique constraint"
    ):
        test_db_session.flush()


def test_organisation_create_then_delete_from_database(
    test_db_session, sample_organisation_object
):
    """Tests creating then deleting an organisation from the database"""
    test_db_session.add(sample_organisation_object)
    test_db_session.flush()

    assert sample_organisation_object.id is not None
    created_org = (
        test_db_session.query(Organisation)
        .filter_by(id=sample_organisation_object.id)
        .first()
    )

    assert created_org is not None
    assert created_org.name == sample_organisation_object.name

    test_db_session.delete(sample_organisation_object)
    test_db_session.flush()

    deleted_org = (
        test_db_session.query(Organisation).filter_by(id=created_org.id).first()
    )

    assert deleted_org is None


def test_create_then_update_from_database(test_db_session, sample_organisation_object):
    test_db_session.add(sample_organisation_object)
    test_db_session.flush()

    assert sample_organisation_object.id is not None
    created_org = (
        test_db_session.query(Organisation)
        .filter_by(id=sample_organisation_object.id)
        .first()
    )

    assert created_org is not None
    assert created_org.name == sample_organisation_object.name

    created_org.name = "New name"
    test_db_session.flush()
    updated_org = (
        test_db_session.query(Organisation).filter_by(id=created_org.id).first()
    )

    assert updated_org.name == "New name"
