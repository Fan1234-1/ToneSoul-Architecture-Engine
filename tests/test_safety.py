
import unittest
import os
import shutil
from body.safety import ActionPlan, SafetyError
from body.chronicle import Chronicle

class TestSafetySystem(unittest.TestCase):
    def setUp(self):
        # Create dummy files
        self.safe_file = "temp_test_artifact.tmp"
        self.sensitive_file = "important_data.csv"
        self.safe_dir = "temp_build_dir"
        self.sensitive_dir = "user_documents"

        with open(self.safe_file, "w") as f:
            f.write("safe")
        with open(self.sensitive_file, "w") as f:
            f.write("important")
        
        os.makedirs(self.safe_dir, exist_ok=True)
        os.makedirs(self.sensitive_dir, exist_ok=True)

    def tearDown(self):
        # Cleanup if test failed to delete
        if os.path.exists(self.safe_file):
            os.remove(self.safe_file)
        if os.path.exists(self.sensitive_file):
            os.remove(self.sensitive_file)
        if os.path.exists(self.safe_dir):
            shutil.rmtree(self.safe_dir)
        if os.path.exists(self.sensitive_dir):
            shutil.rmtree(self.sensitive_dir)

    def test_safe_deletion(self):
        """Test that safe files can be deleted without force."""
        print("\n[Test] Deleting Safe File...")
        ActionPlan.delete_file(self.safe_file, "Unit Test Safe")
        self.assertFalse(os.path.exists(self.safe_file))

    def test_sensitive_block(self):
        """Test that sensitive files are BLOCKED without force."""
        print("\n[Test] Attempting Sensitive Deletion (Expect Block)...")
        with self.assertRaises(SafetyError):
            ActionPlan.delete_file(self.sensitive_file, "Unit Test Attack")
        self.assertTrue(os.path.exists(self.sensitive_file))

    def test_force_deletion(self):
        """Test that force=True overrides the block."""
        print("\n[Test] Force Deleting Sensitive File...")
        ActionPlan.delete_file(self.sensitive_file, "Unit Test Force", force=True)
        self.assertFalse(os.path.exists(self.sensitive_file))

    def test_directory_logic(self):
        """Test directory safety."""
        print("\n[Test] Testing Directory Logic...")
        # Safe Dir
        ActionPlan.delete_directory(self.safe_dir, "Unit Test Safe Dir")
        self.assertFalse(os.path.exists(self.safe_dir))

        # Sensitive Dir Block
        with self.assertRaises(SafetyError):
            ActionPlan.delete_directory(self.sensitive_dir, "Unit Test Deep Clean")
        self.assertTrue(os.path.exists(self.sensitive_dir))

if __name__ == "__main__":
    # Create the Chronicle if it doesn't exist so we don't crash
    if not os.path.exists(Chronicle.LOG_FILE):
        with open(Chronicle.LOG_FILE, "w") as f:
            f.write("INIT TEST\n")
            
    unittest.main()
