import math
import collections
import logging

logger = logging.getLogger(__name__)

class CryptoMonitor:
    @staticmethod
    def calculate_entropy(data: bytes) -> float:
        """Calculates the Shannon entropy of a byte string."""
        if not data:
            return 0
        
        entropy = 0
        counter = collections.Counter(data)
        length = len(data)
        
        for count in counter.values():
            p = count / length
            entropy -= p * math.log2(p)
            
        return entropy

    @staticmethod
    def is_encrypted(file_path: str, threshold: float = 7.5) -> bool:
        """
        Checks if a file has high entropy, suggesting encryption.
        Standard text usually has entropy between 3.5-5.0.
        Compressed/Encrypted data is usually > 7.5 (max is 8.0).
        """
        try:
            with open(file_path, "rb") as f:
                # Read first and last 1MB to save time on huge files
                head = f.read(1024 * 1024)
                # If file is small, head is the whole file
                entropy = CryptoMonitor.calculate_entropy(head)
                
                logger.debug(f"Entropy for {file_path}: {entropy}")
                
                if entropy > threshold:
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to check entropy for {file_path}: {e}")
            return False

if __name__ == "__main__":
    # Test
    import os
    logging.basicConfig(level=logging.DEBUG)
    
    # create a dummy encrypted file (random bytes)
    encrypted_file = "test_encrypted.bin"
    with open(encrypted_file, "wb") as f:
        f.write(os.urandom(1024 * 1024)) # 1MB random noise
        
    print(f"Is {encrypted_file} encrypted? {CryptoMonitor.is_encrypted(encrypted_file)}")
    os.remove(encrypted_file)
    
    # create a dummy text file
    text_file = "test_plain.txt"
    with open(text_file, "w") as f:
        f.write("Hello world " * 10000)
        
    print(f"Is {text_file} encrypted? {CryptoMonitor.is_encrypted(text_file)}")
    os.remove(text_file)
