import time
import argparse
import random

def run_benchmark(iterations: int):
    print(f"Starting benchmark with {iterations} iterations...")
    start_time = time.time()
    
    # Simulate processing
    results = []
    for i in range(iterations):
        time.sleep(0.01) # Simulate network/processing delay
        results.append(random.random())
        
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Benchmark completed in {duration:.2f} seconds.")
    print(f"Average time per iteration: {(duration/iterations)*1000:.2f} ms")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run system benchmarks.")
    parser.add_argument("--iterations", type=int, default=100, help="Number of benchmark iterations")
    args = parser.parse_args()
    
    run_benchmark(args.iterations)
