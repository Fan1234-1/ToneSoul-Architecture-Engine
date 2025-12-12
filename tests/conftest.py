def pytest_ignore_collect(collection_path, config):
    """Ignore files named test_output*.txt during collection."""
    return collection_path.name.startswith("test_output")
