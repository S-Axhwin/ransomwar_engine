import os
import random
import string
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DecoyGenerator:
    def __init__(self, decoy_dir="decoy_files"):
        self.decoy_dir = decoy_dir
        if not os.path.exists(self.decoy_dir):
            os.makedirs(self.decoy_dir)
        self.canary_ledger = {}  # Map filename -> canary_token

    def _generate_random_content(self, size_kb=10):
        """Generates random bytes to simulate file content."""
        return os.urandom(size_kb * 1024)

    def _embed_canary(self, content: bytes, canary: str) -> bytes:
        """Embeds a canary string into the content."""
        # Simple appending for now; in prod, this should be hidden better (e.g., metadata)
        return content + f"\n__CANARY_TOKEN__:{canary}".encode('utf-8')

    def generate_decoy(self, filename: str, ext: str = ".txt"):
        """Creates a decoy file with the given name and extension."""
        full_path = os.path.join(self.decoy_dir, f"{filename}{ext}")
        canary = str(uuid.uuid4())
        
        # Simulate different file structures (basic)
        content = self._generate_random_content(size_kb=random.randint(5, 50))
        final_content = self._embed_canary(content, canary)

        try:
            with open(full_path, "wb") as f:
                f.write(final_content)
            
            self.canary_ledger[full_path] = canary
            logger.info(f"Generated decoy: {full_path} with canary {canary}")
            return full_path
        except Exception as e:
            logger.error(f"Failed to create decoy {full_path}: {e}")
            return None

    def verify_canary(self, file_path: str) -> bool:
        """Checks if the canary is still intact in the file."""
        if file_path not in self.canary_ledger:
            logger.warning(f"File {file_path} is not in ledger.")
            return False
            
        expected_canary = self.canary_ledger[file_path]
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                # Check if our canary token marker exists and matches
                token_marker = b"__CANARY_TOKEN__:"
                if token_marker in content:
                    extracted_canary = content.split(token_marker)[-1].decode('utf-8', errors='ignore').strip()
                    # It might have trailing random bytes if appended, but here we appended it at the end.
                    # Actually, if ransomware encrypts it, this text will be gone.
                    return expected_canary == extracted_canary
                else:
                    return False # Canary missing -> File likely encrypted/overwritten
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return False

if __name__ == "__main__":
    # Test run
    gen = DecoyGenerator(decoy_dir="test_decoys")
    fpath = gen.generate_decoy("salary_report_2024", ".docx")
    print(f"Created: {fpath}")
    print(f"Verification: {gen.verify_canary(fpath)}")
