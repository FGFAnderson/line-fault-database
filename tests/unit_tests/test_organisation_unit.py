from database.models import Organisation

def test_create_organisation_model(sample_organisation_data):
    org = Organisation(**sample_organisation_data)
    
    assert org.name == "Test Organisation"
    assert org.country_code == "EN"
    assert org.region == "South"
    assert org.website == "test.com"
    assert org.logo_url == "test.com/image.png"