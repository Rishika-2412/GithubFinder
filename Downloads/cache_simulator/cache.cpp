#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <algorithm>
#include <unordered_map>
#include <fstream>

class CacheLine {
public:
    bool valid;
    int tag;
    int last_used;

    CacheLine() : valid(false), tag(-1), last_used(0) {}
};

class CacheSimulator {
private:
    int cache_size, block_size, associativity;
    int num_sets;
    std::vector<std::vector<CacheLine>> cache;
    int time, hits, misses;
    std::ofstream output_file;  // For writing results to a file

public:
    CacheSimulator(int cache_size, int block_size, int associativity, const std::string& output_filename)
        : cache_size(cache_size), block_size(block_size), associativity(associativity),
          hits(0), misses(0), time(0) {
        num_sets = cache_size / (block_size * associativity);
        cache.resize(num_sets, std::vector<CacheLine>(associativity));
        
        // Open the file for writing simulation results
        output_file.open(output_filename);
        if (!output_file.is_open()) {
            std::cerr << "Failed to open output file!" << std::endl;
            exit(1);
        }
    }

    ~CacheSimulator() {
        if (output_file.is_open()) {
            output_file.close();
        }
    }

    std::string access(int address) {
        time++;
        int block_number = address / block_size;
        int index = block_number % num_sets;
        int tag = block_number / num_sets;

        // Check for HIT
        for (auto& line : cache[index]) {
            if (line.valid && line.tag == tag) {
                hits++;
                line.last_used = time;
                return "HIT";
            }
        }

        // MISS handling
        misses++;
        for (auto& line : cache[index]) {
            if (!line.valid) {
                line.valid = true;
                line.tag = tag;
                line.last_used = time;
                return "MISS";
            }
        }

        // LRU replacement
        auto lru_line = std::min_element(cache[index].begin(), cache[index].end(),
            [](const CacheLine& a, const CacheLine& b) {
                return a.last_used < b.last_used;
            });
        lru_line->tag = tag;
        lru_line->last_used = time;
        return "MISS";
    }

    void simulate(const std::vector<int>& address_trace) {
        std::vector<std::pair<int, std::string>> result_trace;

        for (int address : address_trace) {
            result_trace.push_back({address, access(address)});
        }

        // Write results to output file
        for (const auto& result : result_trace) {
            output_file << "Address: " << result.first << " -> " << result.second << std::endl;
        }

        int total_accesses = hits + misses;
        double hit_rate = (hits / (double)total_accesses) * 100;
        double miss_rate = (misses / (double)total_accesses) * 100;

        output_file << "\nTotal Accesses: " << total_accesses
                    << "\nHits: " << hits
                    << "\nMisses: " << misses
                    << "\nHit Rate: " << hit_rate << "%"
                    << "\nMiss Rate: " << miss_rate << "%" << std::endl;
    }
};

int main() {
    srand(time(0));  // Seed for random generation
    CacheSimulator cache_sim(128, 4, 2, "cache_simulation_results.txt");

    std::vector<int> addresses(100);
    for (int& address : addresses) {
        address = rand() % 256;
    }

    // Simulate the cache accesses
    cache_sim.simulate(addresses);

    std::cout << "Simulation complete. Results are written to 'cache_simulation_results.txt'" << std::endl;

    return 0;
}