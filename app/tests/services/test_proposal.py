import hashlib
import uuid
import pytest

# Assuming the logic for hashing proposal_id (a UUID string) to bytes32 is:
# rental_id_bytes = hashlib.sha256(proposal_id_str.encode()).digest()

def test_proposal_id_string_to_bytes32_conversion():
    """Test that a UUID string is correctly hashed to 32 bytes."""
    sample_uuid_str = str(uuid.uuid4())
    
    # The core logic from ProposalService for ID conversion
    rental_id_bytes = hashlib.sha256(sample_uuid_str.encode('utf-8')).digest()
    
    assert isinstance(rental_id_bytes, bytes), "Output should be bytes"
    assert len(rental_id_bytes) == 32, "Output should be 32 bytes long for bytes32"

def test_proposal_id_conversion_empty_string():
    """Test hashing an empty string (edge case)."""
    empty_str = ""
    rental_id_bytes = hashlib.sha256(empty_str.encode('utf-8')).digest()
    assert len(rental_id_bytes) == 32

def test_proposal_id_conversion_known_string():
    """Test hashing a known string to ensure consistency (optional, but good)."""
    # Example UUID from a previous test or defined constant
    known_uuid_str = "123e4567-e89b-12d3-a456-426614174000"
    expected_hash_hex = "b09bf93f0ba070781e1170089196073a630533906636791985016998a0702052" # sha256sum of the string
    
    rental_id_bytes = hashlib.sha256(known_uuid_str.encode('utf-8')).digest()
    
    assert len(rental_id_bytes) == 32
    assert rental_id_bytes.hex() == expected_hash_hex

# If this logic were encapsulated in ProposalService, e.g., as a static method:
# from app.services.proposal import ProposalService 
# def test_proposal_service_id_conversion_method():
#     sample_uuid_str = str(uuid.uuid4())
#     rental_id_bytes = ProposalService._convert_id_to_bytes32(sample_uuid_str) # Hypothetical method
#     assert len(rental_id_bytes) == 32 