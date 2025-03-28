"""Independent test that doesn't rely on conftest.py."""

def test_independent():
    """A simple test that doesn't depend on any fixtures."""
    assert 1 + 1 == 2
    assert "Smart Rent" in "This is the Smart Rent Platform"
    assert isinstance("test", str)
    assert len([1, 2, 3]) == 3 