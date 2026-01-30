import time
import os
import threading
from ransomware_engine.decoy.generator import DecoyGenerator
from ransomware_engine.detector.fim import FIMMonitor

def alert(path, reason):
    print(f"!!! ALERT RECEIVED: {reason} -> {path}")

def run_test():
    # 1. Setup Decoys
    print("Generating decoys...")
    gen = DecoyGenerator("test_decoys_fim")
    decoy_path = gen.generate_decoy("secret_plans", ".docx")
    decoy_abs_path = os.path.abspath(decoy_path)
    
    ledger = {decoy_abs_path: gen.canary_ledger[decoy_path]}
    
    # 2. Start FIM
    print("Starting FIM...")
    fim = FIMMonitor(".", ledger, alert)
    fim.start()
    
    time.sleep(2)
    
    # 3. Simulate Ransomware Attack (Append bytes)
    print(f"Modifying {decoy_abs_path}...")
    with open(decoy_abs_path, "ab") as f:
        f.write(b"ENCRYPTED_DATA_JUNK")
        
    time.sleep(2)
    
    # 4. Stop
    fim.stop()
    print("Test Complete.")

if __name__ == "__main__":
    run_test()
