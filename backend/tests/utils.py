"""Utility functions for Smart Rent Platform API tests."""
import random
import string
from datetime import datetime, timedelta

from ..app.models import UserRole, UserStatus, PropertyStatus, ContractStatus, User, Property, Contract


def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def random_email():
    """Generate a random email address."""
    name = random_string(8)
    domain = random_string(6)
    return f"{name}@{domain}.com"


def random_wallet_address():
    """Generate a random Ethereum wallet address."""
    # Format: 0x + 40 hex characters
    hex_chars = string.hexdigits.lower()[:16]
    address = '0x' + ''.join(random.choice(hex_chars) for _ in range(40))
    return address


def create_test_user(db, role=UserRole.TENANT, status=UserStatus.APPROVED):
    """Create a test user with random data."""
    user = User(
        email=random_email(),
        hashed_password="$2b$12$HxjEkIgt9.Y/xaRYbVw8XOTf1BNIYHzHLVO55zWKgcQZ6yvKpUzNW",  # password = 'Password123'
        full_name=f"Test {role.value.capitalize()} {random_string(5)}",
        role=role,
        status=status,
        wallet_address=random_wallet_address() if random.choice([True, False]) else None,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_property(db, owner_id, status=PropertyStatus.APPROVED):
    """Create a test property with random data."""
    bedrooms = random.randint(1, 5)
    bathrooms = random.randint(1, 3)
    sqft = random.randint(500, 3000)
    price = random.randint(50000, 300000)  # $500-$3000 (stored in cents)
    
    property_item = Property(
        title=f"Test Property {random_string(5)}",
        description=f"A {bedrooms} bedroom, {bathrooms} bathroom property with {sqft} sqft",
        address=f"{random.randint(100, 999)} {random_string(8).capitalize()} St, {random_string(6).capitalize()}, {random_string(2).upper()} {random.randint(10000, 99999)}",
        price=price,
        owner_id=owner_id,
        status=status,
        images=[f"http://example.com/image{i}.jpg" for i in range(1, random.randint(2, 5))],
        features={"bedrooms": bedrooms, "bathrooms": bathrooms, "sqft": sqft},
        created_at=datetime.now()
    )
    db.add(property_item)
    db.commit()
    db.refresh(property_item)
    return property_item


def create_test_contract(db, property_id, tenant_id, landlord_id, status=ContractStatus.PENDING):
    """Create a test contract with random data."""
    start_date = datetime.now() + timedelta(days=random.randint(7, 30))
    end_date = start_date + timedelta(days=random.randint(180, 365))
    
    # Get property price for rent
    property_item = db.query(Property).filter(Property.id == property_id).first()
    monthly_rent = property_item.price if property_item else random.randint(50000, 300000)
    security_deposit = monthly_rent * 2
    
    contract = Contract(
        property_id=property_id,
        tenant_id=tenant_id,
        landlord_id=landlord_id,
        start_date=start_date,
        end_date=end_date,
        monthly_rent=monthly_rent,
        security_deposit=security_deposit,
        status=status,
        blockchain_address=random_wallet_address() if random.choice([True, False]) else None,
        created_at=datetime.now()
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def assert_keys_in_dict(expected_keys, dictionary):
    """Assert that all expected keys are in the dictionary."""
    for key in expected_keys:
        assert key in dictionary, f"Key '{key}' not found in response" 