"""
Demonstration of packet dropping with finite queue capacity.

This shows how different strategies handle congestion when queues are limited.
"""

from queuing_strategies import FCFSQueue, FairQueue
from simulation import PacketGenerator, Simulator
import copy

def demonstrate_packet_dropping():
    """Demonstrate packet dropping with limited queue capacity."""
    
    print("="*100)
    print("PACKET DROPPING DEMONSTRATION")
    print("="*100)
    print("\nScenario: High traffic load with LIMITED queue capacity")
    print("  • Queue capacity: 20 packets")
    print("  • Traffic: 100 packets with bursty arrivals")
    print("  • Shows which strategy handles congestion better")
    print("="*100)
    
    # Generate high-load bursty traffic
    generator = PacketGenerator(seed=42)
    packets = generator.generate_packets(
        num_packets=100,
        arrival_rate=5.0,  # High arrival rate
        priority_distribution={1: 0.6, 2: 0.3, 3: 0.1},
        traffic_model='bursty'
    )
    
    print(f"\nGenerated {len(packets)} packets")
    
    # Count packets per flow
    flow_counts = {}
    for p in packets:
        flow_counts[p.priority] = flow_counts.get(p.priority, 0) + 1
    
    print(f"Packet distribution:")
    for fid in sorted(flow_counts.keys()):
        print(f"  Flow {fid}: {flow_counts[fid]} packets")
    
    # Test with different queue sizes
    queue_sizes = [None, 50, 20]  # None = infinite, 50 = moderate, 20 = small
    
    for queue_size in queue_sizes:
        print(f"\n{'='*100}")
        if queue_size is None:
            print(f"Queue Capacity: INFINITE (no drops)")
        else:
            print(f"Queue Capacity: {queue_size} packets (drops when full)")
        print(f"{'='*100}")
        
        strategies = [
            ("FCFS", FCFSQueue(max_queue_size=queue_size)),
            ("Fair Queue", FairQueue(max_queue_size=queue_size))
        ]
        
        for name, strategy in strategies:
            # Reset packets
            packet_copies = [copy.copy(p) for p in packets]
            for p in packet_copies:
                p.start_time = None
                p.finish_time = None
            
            # Run simulation
            simulator = Simulator(strategy)
            simulator.run(packet_copies)
            
            # Get metrics
            metrics = strategy.get_metrics()
            
            print(f"\n{name}:")
            print(f"  Processed:  {metrics['total_packets']} packets")
            print(f"  Dropped:    {metrics['dropped_packets']} packets ({metrics['drop_rate']*100:.1f}%)")
            print(f"  Avg Latency: {metrics['avg_latency']:.2f}s")
            print(f"  Flow Fairness: {metrics['flow_fairness_index']:.4f}")
            
            # Show per-flow drops
            if metrics['dropped_packets'] > 0:
                flow_drops = {}
                for p in strategy.dropped_packets:
                    flow_drops[p.priority] = flow_drops.get(p.priority, 0) + 1
                
                print(f"  Drops by flow:")
                for fid in sorted(flow_drops.keys()):
                    pct = (flow_drops[fid] / flow_counts[fid]) * 100
                    print(f"    Flow {fid}: {flow_drops[fid]}/{flow_counts[fid]} ({pct:.1f}%)")
    
    print("\n" + "="*100)
    print("KEY INSIGHTS:")
    print("="*100)
    print("""
With INFINITE queue capacity:
  • No packets dropped
  • All strategies process all packets
  • Fair Queue shows best flow fairness

With LIMITED queue capacity (congestion):
  • Packets are dropped when queue is full
  • Drop rate shows how well strategy handles overload
  • Fair Queue may provide more balanced drops across flows
  
REAL-WORLD RELEVANCE:
  • Routers have finite buffer memory
  • During congestion, packets must be dropped
  • Fair dropping protects small flows from being starved
  • Important for QoS in production networks
""")
    print("="*100)

if __name__ == "__main__":
    demonstrate_packet_dropping()
