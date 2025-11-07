"""
Example script demonstrating how to use the QoS queuing strategies.

This is a simple example showing how to:
1. Generate packets
2. Run simulations with different strategies
3. Compare results
"""

from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue
from simulation import PacketGenerator, run_experiment
from visualization import print_results_table

def main():
    print("="*80)
    print("QoS Queuing Strategies - Simple Example")
    print("="*80)
    
    # Step 1: Generate packets
    print("\n1. Generating 50 packets with varying priorities...")
    generator = PacketGenerator(seed=100)
    packets = generator.generate_packets(
        num_packets=50,
        arrival_rate=2.0,
        priority_distribution={1: 0.4, 2: 0.4, 3: 0.2}
    )
    print(f"   ✓ Generated {len(packets)} packets")
    print(f"   Sample packet: {packets[0]}")
    
    # Step 2: Create queuing strategies
    print("\n2. Creating queuing strategies...")
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5)
    ]
    print(f"   ✓ Created {len(strategies)} strategies: FCFS, Priority Queue, Round-Robin")
    
    # Step 3: Run experiment
    print("\n3. Running simulation...")
    results = run_experiment(packets, strategies)
    print("   ✓ Simulation complete")
    
    # Step 4: Display results
    print("\n4. Performance Results:")
    print_results_table(results)
    
    # Step 5: Analysis
    print("5. Quick Analysis:")
    print("-" * 80)
    
    for strategy_name, metrics in results.items():
        print(f"\n{strategy_name}:")
        print(f"  • Processed {metrics['total_packets']} packets")
        print(f"  • Average latency: {metrics['avg_latency']:.2f} seconds")
        print(f"  • Throughput: {metrics['throughput']:.2f} packets/second")
        print(f"  • Fairness index: {metrics['fairness_index']:.3f} (higher is better)")
    
    print("\n" + "="*80)
    print("Example complete! Run 'python main.py' for comprehensive experiments.")
    print("="*80)

if __name__ == "__main__":
    main()
