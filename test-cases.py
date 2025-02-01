import unittest
from unittest.mock import patch
from main import list_s3_objects


class TestS3Functions(unittest.TestCase):

    def setUp(self):
        """Setup mock data for S3 responses."""
        self.mock_s3_response_top = {"Contents": [{"Key": "dir1/"}, {"Key": "dir2/"}]}
        self.mock_s3_response_subdir = {
            "Contents": [{"Key": "dir2/file1"}, {"Key": "dir2/file2"}]
        }

    @patch("main.s3_client.list_objects_v2")
    def test_list_top_level_content(self, mock_s3):
        """Test listing top-level contents of S3 bucket."""
        mock_s3.return_value = self.mock_s3_response_top
        result = list_s3_objects()
        self.assertEqual(result, {"content": ["dir1", "dir2"]})

    @patch("main.s3_client.list_objects_v2")
    def test_list_files_in_directory(self, mock_s3):
        """Test listing files inside a directory."""
        mock_s3.return_value = self.mock_s3_response_subdir
        result = list_s3_objects("dir2")
        self.assertEqual(result, {"content": ["file1", "file2"]})


if __name__ == "__main__":
    unittest.main()