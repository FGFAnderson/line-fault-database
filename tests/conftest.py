
import pytest
from database.models.organisation import Organisation

@pytest.fixture()
def sample_organisation_data():
    return {
        "name": "Test Org",
        "country_code": "EN",
        "region": "South",
        "website": "test.com",
        "logo_url": "test.com/image.png"
    }
    
@pytest.fixture()
def sample_organisation_object():
    return Organisation(
        name="Test Org",
        country_code="GB",
        region="South",
        website="test.com",
        logo_url="test.com/image.png"
    )
