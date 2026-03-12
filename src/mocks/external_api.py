import random
import time

class ExternalBureau:
    def __init__(self):
        pass

    def call_with_retry(self, request_id, retries=3):
        """
        Simulates an external API with random failures.
        Fulfills 'Engineering Robustness' requirement (Retry Flow).
        """
        for i in range(retries):
            # Simulate a 40% chance of a temporary network failure
            if random.random() < 0.4:
                print(f"  [Attempt {i+1}] External API Timeout... Retrying.")
                time.sleep(1)  # Exponential backoff simulation
                continue
            
            # If successful, return mock credit data
            print(f"  [Attempt {i+1}] External API Success!")
            return {"score": 750, "credit_status": "ACTIVE"}
        
        # If all retries fail
        raise Exception("External Service Unavailable after max retries")