# Import path library
from pathlib import Path

from src.data.PrepareInput import PrepareAudio as pa


class TestPrepareAudio():
    """Tests the PrepareAudio class in src/data
    """

    def test_mp3_file_accepted(self):
        """Test that a valid mp3 file is accepted"""
        file = Path("tests/test_data/validfile_1.mp3")
        assert pa.check_file_type(file) is True
