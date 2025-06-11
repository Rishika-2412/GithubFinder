import random
import pandas as pd
import matplotlib.pyplot as plt

class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = None
        self.last_used = 0  # for LRU tracking

class CacheSimulator:
    def __init__(self, cache_size, block_size, associativity, replacement_policy="LRU"):
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.num_sets = cache_size // (block_size * associativity)
        self.cache = [[CacheLine() for _ in range(associativity)] for _ in range(self.num_sets)]
        self.time = 0
        self.hits = 0
        self.misses = 0

    def access(self, address):
        self.time += 1
        block_number = address // self.block_size
        index = block_number % self.num_sets
        tag = block_number // self.num_sets

        # Check for HIT
        for line in self.cache[index]:
            if line.valid and line.tag == tag:
                self.hits += 1
                line.last_used = self.time
                return "HIT"

        # MISS handling
        self.misses += 1
        for line in self.cache[index]:
            if not line.valid:
                line.valid = True
                line.tag = tag
                line.last_used = self.time
                return "MISS"

        # Replacement using LRU
        if self.replacement_policy == "LRU":
            lru_line = min(self.cache[index], key=lambda x: x.last_used)
            lru_line.tag = tag
            lru_line.last_used = self.time
            return "MISS"

    def simulate(self, address_trace):
        results = []
        hit_rates = []
        miss_rates = []

        for i, address in enumerate(address_trace):
            result = self.access(address)
            results.append((address, result))

            # Calculate current hit and miss rates
            total_accesses = self.hits + self.misses
            hit_rate = (self.hits / total_accesses * 100) if total_accesses else 0
            miss_rate = (self.misses / total_accesses * 100) if total_accesses else 0
            hit_rates.append(hit_rate)
            miss_rates.append(miss_rate)

        return results, hit_rates, miss_rates

    def stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total * 100 if total else 0
        miss_rate = self.misses / total * 100 if total else 0
        return {
            "Total Accesses": total,
            "Hits": self.hits,
            "Misses": self.misses,
            "Hit Rate (%)": hit_rate,
            "Miss Rate (%)": miss_rate
        }

# Sample test run
if __name__ == "__main__":
    cache_sim = CacheSimulator(cache_size=128, block_size=4, associativity=2)
    addresses = [random.randint(0, 256) for _ in range(100)]
    result_trace, hit_rates, miss_rates = cache_sim.simulate(addresses)

    print("Generated address trace:", addresses[:10])
    stats = cache_sim.stats()

    # Output results
    result_df = pd.DataFrame(result_trace, columns=["Address", "Result"])
    print(result_df.head())
    print("\nStats:", stats)

    # Plotting Hit and Miss rates
    plt.figure(figsize=(10, 6))
    plt.plot(hit_rates, label="Hit Rate (%)", color='g')
    plt.plot(miss_rates, label="Miss Rate (%)", color='r')
    plt.xlabel('Accesses')
    plt.ylabel('Percentage')
    plt.title('Hit and Miss Rates Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()