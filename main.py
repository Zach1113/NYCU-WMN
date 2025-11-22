"""
Main simulation runner for QoS queuing strategies.

This script runs comprehensive experiments comparing FCFS, Priority Queue,
Round-Robin, and Fair Queueing strategies under various traffic conditions.
"""

import os
import copy
from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue, FairQueue
from simulation import PacketGenerator, Simulator, run_experiment
from visualization import (plot_comparison, plot_all_metrics, 
                          plot_latency_distribution, plot_priority_fairness,
                          print_results_table)


def run_basic_experiment():
    """Run basic experiment with moderate traffic."""
    print("\n" + "="*80)
    print("EXPERIMENT 1: Basic Comparison (Moderate Traffic)")
    print("="*80)
    
    # Generate packets
    generator = PacketGenerator(seed=42)
    packets = generator.generate_packets(
        num_packets=100,
        arrival_rate=2.0,
        priority_distribution={1: 0.5, 2: 0.3, 3: 0.2}
    )
    
    # Create strategies
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5),
        FairQueue()
    ]
    
    # Run experiment
    results = run_experiment(packets, strategies)
    
    # Print results
    print_results_table(results)
    
    # Create visualizations
    os.makedirs('results', exist_ok=True)
    plot_all_metrics(results, save_path='results/basic_comparison.png')
    
    return results, strategies


def run_high_traffic_experiment():
    """Run experiment with high traffic load."""
    print("\n" + "="*80)
    print("EXPERIMENT 2: High Traffic Load")
    print("="*80)
    
    # Generate many packets with high arrival rate
    generator = PacketGenerator(seed=43)
    packets = generator.generate_packets(
        num_packets=500,
        arrival_rate=5.0,  # High arrival rate
        priority_distribution={1: 0.6, 2: 0.3, 3: 0.1}
    )
    
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5),
        FairQueue()
    ]
    
    results = run_experiment(packets, strategies)
    print_results_table(results)
    
    plot_comparison(results, metric='avg_latency', 
                   title='High Traffic - Average Latency Comparison',
                   save_path='results/high_traffic_latency.png')
    
    return results


def run_priority_stress_test():
    """Run experiment with varied priority distributions."""
    print("\n" + "="*80)
    print("EXPERIMENT 3: Priority Distribution Stress Test")
    print("="*80)
    
    # Generate packets with more high-priority packets
    generator = PacketGenerator(seed=44)
    packets = generator.generate_packets(
        num_packets=200,
        arrival_rate=2.5,
        priority_distribution={1: 0.2, 2: 0.3, 3: 0.5}  # Many high-priority
    )
    
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5),
        FairQueue()
    ]
    
    results = run_experiment(packets, strategies)
    print_results_table(results)
    
    # Analyze fairness for Priority Queue strategy
    pq_strategy = PriorityQueue()
    simulator = Simulator(pq_strategy)
    packet_copies = [copy.copy(p) for p in packets]
    for p in packet_copies:
        p.start_time = None
        p.finish_time = None
    simulator.run(packet_copies)
    
    # Group packets by priority
    packets_by_priority = {}
    for p in pq_strategy.processed_packets:
        if p.priority not in packets_by_priority:
            packets_by_priority[p.priority] = []
        packets_by_priority[p.priority].append(p)
    
    plot_priority_fairness(packets_by_priority, 'Priority Queue',
                          save_path='results/priority_fairness.png')
    
    return results


def run_variable_service_time_experiment():
    """Run experiment with variable service times."""
    print("\n" + "="*80)
    print("EXPERIMENT 4: Variable Service Times")
    print("="*80)
    
    # Generate packets with wide range of service times
    generator = PacketGenerator(seed=45)
    packets = generator.generate_packets(
        num_packets=150,
        arrival_rate=2.0,
        priority_distribution={1: 0.4, 2: 0.4, 3: 0.2},
        service_time_range=(0.1, 5.0)  # Wide range
    )
    
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5),
        FairQueue()
    ]
    
    results = run_experiment(packets, strategies)
    print_results_table(results)
    
    plot_comparison(results, metric='fairness_index',
                   title='Variable Service Times - Fairness Comparison',
                   save_path='results/variable_service_fairness.png')
    
    return results


def run_latency_distribution_analysis():
    """Analyze latency distribution across strategies."""
    print("\n" + "="*80)
    print("EXPERIMENT 5: Latency Distribution Analysis")
    print("="*80)
    
    generator = PacketGenerator(seed=46)
    packets = generator.generate_packets(
        num_packets=200,
        arrival_rate=2.0,
        priority_distribution={1: 0.4, 2: 0.3, 3: 0.3}
    )
    
    strategies = [
        FCFSQueue(),
        PriorityQueue(),
        RoundRobinQueue(num_queues=3, time_quantum=0.5),
        FairQueue()
    ]
    
    # Run each strategy and collect processed packets
    strategies_packets = {}
    for strategy in strategies:
        packet_copies = [copy.copy(p) for p in packets]
        for p in packet_copies:
            p.start_time = None
            p.finish_time = None
        
        simulator = Simulator(strategy)
        simulator.run(packet_copies)
        strategies_packets[strategy.name] = strategy.processed_packets
    
    plot_latency_distribution(strategies_packets, 
                             save_path='results/latency_distribution.png')
    
    print("Latency distribution analysis complete.")


def main():
    """Run all experiments and generate comprehensive analysis."""
    print("\n" + "="*80)
    print("QoS QUEUING STRATEGIES SIMULATION")
    print("Comparing FCFS, Priority Queue, Round-Robin, and Fair Queue")
    print("="*80)
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Run all experiments
    print("\nRunning comprehensive experiments...")
    
    results1, strategies = run_basic_experiment()
    results2 = run_high_traffic_experiment()
    results3 = run_priority_stress_test()
    results4 = run_variable_service_time_experiment()
    run_latency_distribution_analysis()
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETE")
    print("="*80)
    print("\nResults and visualizations saved to 'results/' directory:")
    print("  - basic_comparison.png: Overall performance comparison")
    print("  - high_traffic_latency.png: Performance under high load")
    print("  - priority_fairness.png: Fairness analysis for Priority Queue")
    print("  - variable_service_fairness.png: Fairness with variable service times")
    print("  - latency_distribution.png: Latency distribution comparison")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
