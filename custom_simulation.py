"""
Interactive script to run custom QoS simulations with user-defined parameters.

This script allows you to customize:
- Number of packets
- Arrival rate
- Priority distribution
- Service time ranges
"""

import sys
from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue
from simulation import PacketGenerator, run_experiment
from visualization import print_results_table, plot_all_metrics


def run_custom_simulation(num_packets=100, arrival_rate=2.0, 
                         high_priority_ratio=0.2, seed=42):
    """
    Run a custom simulation with specified parameters.
    
    Args:
        num_packets: Number of packets to generate
        arrival_rate: Packets per time unit (higher = more congestion)
        high_priority_ratio: Ratio of high-priority packets (0.0 to 1.0)
        seed: Random seed for reproducibility
    """
    print("\n" + "="*80)
    print("CUSTOM QoS SIMULATION")
    print("="*80)
    print(f"\nParameters:")
    print(f"  • Packets: {num_packets}")
    print(f"  • Arrival rate: {arrival_rate} packets/second")
    print(f"  • High priority ratio: {high_priority_ratio:.1%}")
    print(f"  • Random seed: {seed}")
    
    # Calculate priority distribution
    low_priority = (1 - high_priority_ratio) * 0.6
    medium_priority = (1 - high_priority_ratio) * 0.4
    priority_dist = {
        1: low_priority,
        2: medium_priority,
        3: high_priority_ratio
    }
    
    # Generate packets
    print("\nGenerating packets...")
    generator = PacketGenerator(seed=seed)
    packets = generator.generate_packets(
        num_packets=num_packets,
        arrival_rate=arrival_rate,
        priority_distribution=priority_dist
    )
    
    # Create strategies
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5)
    ]
    
    # Run simulation
    print("Running simulation...")
    results = run_experiment(packets, strategies)
    
    # Display results
    print_results_table(results)
    
    # Generate visualization
    output_file = f'results/custom_sim_{num_packets}p_{arrival_rate}r_{high_priority_ratio}hp.png'
    plot_all_metrics(results, save_path=output_file)
    print(f"\nVisualization saved to: {output_file}")
    
    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    best_latency = min(results.items(), key=lambda x: x[1]['avg_latency'])
    best_fairness = max(results.items(), key=lambda x: x[1]['fairness_index'])
    
    print(f"\n• Best Average Latency: {best_latency[0]} ({best_latency[1]['avg_latency']:.2f}s)")
    print(f"• Best Fairness: {best_fairness[0]} ({best_fairness[1]['fairness_index']:.3f})")
    
    if high_priority_ratio > 0.3:
        print("\n• With high priority traffic, Priority Queue is recommended")
        print("  for latency-sensitive applications.")
    elif arrival_rate > 3.0:
        print("\n• Under high load, Round-Robin provides better fairness")
        print("  and prevents queue starvation.")
    else:
        print("\n• With moderate traffic, FCFS provides good balance")
        print("  of simplicity and fairness.")
    
    print("\n" + "="*80 + "\n")
    
    return results


def interactive_mode():
    """Run in interactive mode with user input."""
    print("="*80)
    print("QoS SIMULATION - INTERACTIVE MODE")
    print("="*80)
    
    try:
        num_packets = int(input("\nNumber of packets (default 100): ") or "100")
        arrival_rate = float(input("Arrival rate in packets/sec (default 2.0): ") or "2.0")
        high_priority = float(input("High priority ratio 0-1 (default 0.2): ") or "0.2")
        seed = int(input("Random seed (default 42): ") or "42")
        
        run_custom_simulation(num_packets, arrival_rate, high_priority, seed)
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSimulation cancelled by user.")
        sys.exit(0)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Command line mode
        if len(sys.argv) == 5:
            num_packets = int(sys.argv[1])
            arrival_rate = float(sys.argv[2])
            high_priority = float(sys.argv[3])
            seed = int(sys.argv[4])
            run_custom_simulation(num_packets, arrival_rate, high_priority, seed)
        else:
            print("Usage:")
            print("  Interactive mode: python custom_simulation.py")
            print("  Command line: python custom_simulation.py <num_packets> <arrival_rate> <high_priority_ratio> <seed>")
            print("\nExample:")
            print("  python custom_simulation.py 200 3.0 0.3 42")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
