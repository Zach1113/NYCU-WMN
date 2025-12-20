"""
Realistic Packet Dropping Scenarios

This demonstrates how different queuing strategies handle real-world traffic patterns:
1. Message Texting - Small, bursty, low priority
2. Video Streaming - Large chunks, high bandwidth, medium priority
3. Online Meeting - Real-time, constant rate, high priority
4. File Download - Bulk transfer, aggressive, low priority
"""

from queuing_strategies import FCFSQueue, FairQueue, LASQueue
from simulation import PacketGenerator, Simulator
from packet import Packet
import copy
import random


def generate_scenario_traffic(scenario_name, seed=42):
    """
    Generate traffic patterns for different real-world scenarios.
    
    Returns:
        List of packets with realistic characteristics for the scenario
    """
    random.seed(seed)
    packets = []
    packet_id = 0
    
    if scenario_name == "message_texting":
        # Scenario 1: Message Texting
        # - Small packets (text messages are tiny)
        # - Very bursty (user types, sends, waits)
        # - Low bandwidth requirement
        # - 3 users sending messages
        print("\n📱 SCENARIO: Message Texting")
        print("   • 3 users sending text messages")
        print("   • Small packets (100-500 bytes)")
        print("   • Very bursty arrivals")
        
        for user_id in range(1, 4):  # 3 users
            # Each user sends 5-15 messages in bursts
            num_messages = random.randint(5, 15)
            base_time = random.uniform(0, 2)  # Start time offset
            
            for msg in range(num_messages):
                packets.append(Packet(
                    packet_id=packet_id,
                    arrival_time=base_time + msg * random.uniform(0.1, 0.5),
                    priority=user_id,
                    size=random.randint(100, 500),  # Small text packets
                    service_time=random.uniform(0.01, 0.05)  # Quick to process
                ))
                packet_id += 1
                
    elif scenario_name == "video_streaming":
        # Scenario 2: Video Streaming (Netflix/YouTube style)
        # - Large packets (video chunks)
        # - Constant high bandwidth
        # - Multiple quality levels (flows)
        print("\n📺 SCENARIO: Video Streaming")
        print("   • 2 streams: HD (1080p) and SD (480p)")
        print("   • Large packets (video chunks)")
        print("   • Continuous high bandwidth demand")
        
        # HD Stream (priority 1) - more packets, larger
        for i in range(50):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.1,  # Regular intervals
                priority=1,  # HD stream
                size=random.randint(3000, 5000),  # Large video chunks
                service_time=random.uniform(0.3, 0.5)
            ))
            packet_id += 1
        
        # SD Stream (priority 2) - fewer packets, smaller
        for i in range(30):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.15 + 0.05,  # Offset slightly
                priority=2,  # SD stream
                size=random.randint(1000, 2000),
                service_time=random.uniform(0.1, 0.2)
            ))
            packet_id += 1
            
    elif scenario_name == "online_meeting":
        # Scenario 3: Online Meeting (Zoom/Teams style)
        # - Mixed audio and video packets
        # - Real-time requirements (low latency critical)
        # - Multiple participants
        print("\n💻 SCENARIO: Online Meeting (Video Conference)")
        print("   • 3 participants with audio + video")
        print("   • Real-time traffic (latency sensitive)")
        print("   • Mixed packet sizes")
        
        for participant in range(1, 4):  # 3 participants
            # Audio packets (small, frequent, high priority behavior)
            for i in range(30):
                packets.append(Packet(
                    packet_id=packet_id,
                    arrival_time=i * 0.05 + participant * 0.01,
                    priority=participant,
                    size=random.randint(200, 400),  # Small audio packets
                    service_time=random.uniform(0.02, 0.05)
                ))
                packet_id += 1
            
            # Video packets (larger, less frequent)
            for i in range(15):
                packets.append(Packet(
                    packet_id=packet_id,
                    arrival_time=i * 0.2 + participant * 0.02,
                    priority=participant,
                    size=random.randint(1500, 3000),
                    service_time=random.uniform(0.1, 0.2)
                ))
                packet_id += 1
                
    elif scenario_name == "file_download":
        # Scenario 4: File Download (Bulk Transfer)
        # - Very large packets
        # - One dominant flow (the downloader)
        # - Competes with smaller background traffic
        print("\n📥 SCENARIO: File Download with Background Traffic")
        print("   • 1 large file download (aggressive)")
        print("   • 2 small background tasks")
        print("   • Tests flow starvation")
        
        # Large file download (Flow 1) - AGGRESSIVE, many large packets
        for i in range(60):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.05,  # Very fast arrival
                priority=1,
                size=random.randint(4000, 5000),  # Maximum size
                service_time=random.uniform(0.4, 0.6)
            ))
            packet_id += 1
        
        # Background task 1 (Flow 2) - small, occasional
        for i in range(15):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.3 + 0.1,
                priority=2,
                size=random.randint(500, 1000),
                service_time=random.uniform(0.05, 0.1)
            ))
            packet_id += 1
        
        # Background task 2 (Flow 3) - small, occasional
        for i in range(10):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.4 + 0.2,
                priority=3,
                size=random.randint(500, 1000),
                service_time=random.uniform(0.05, 0.1)
            ))
            packet_id += 1
    
    elif scenario_name == "mice_and_elephants":
        # Scenario 5: Web Browsing with Background Downloads
        # This is where LAS should shine!
        # - Elephant flows: Large continuous downloads
        # - Mice flows: Small sporadic web requests that need quick response
        print("\n🐘🐭 SCENARIO: Mice and Elephants (Web + Downloads)")
        print("   • 2 elephant flows: Large continuous downloads")
        print("   • 10 mice flows: Small web requests arriving over time")
        print("   • LAS should protect mice by prioritizing least-served flows")
        
        # Elephant 1: Large download (Flow 1) - starts immediately, continuous
        for i in range(40):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.08,  # Continuous stream
                priority=1,
                size=random.randint(4000, 5000),
                service_time=random.uniform(0.4, 0.6)
            ))
            packet_id += 1
        
        # Elephant 2: Another download (Flow 2) - starts slightly later
        for i in range(35):
            packets.append(Packet(
                packet_id=packet_id,
                arrival_time=i * 0.09 + 0.5,
                priority=2,
                size=random.randint(4000, 5000),
                service_time=random.uniform(0.4, 0.6)
            ))
            packet_id += 1
        
        # Mice flows (Flows 3-12): Small web requests arriving sporadically
        # These are the flows that LAS should protect!
        for mouse_id in range(3, 13):  # 10 mice flows
            # Each mouse sends only 2-4 small packets
            num_packets = random.randint(2, 4)
            start_time = random.uniform(0.2, 2.5)  # Arrive at different times
            
            for i in range(num_packets):
                packets.append(Packet(
                    packet_id=packet_id,
                    arrival_time=start_time + i * 0.02,  # Very close together
                    priority=mouse_id,
                    size=random.randint(200, 500),  # Small web packets
                    service_time=random.uniform(0.02, 0.05)  # Quick to process
                ))
                packet_id += 1
    
    # Sort by arrival time
    packets.sort(key=lambda p: p.arrival_time)
    return packets


def run_scenario(scenario_name, queue_size=30):
    """Run a single scenario with all three strategies."""
    
    packets = generate_scenario_traffic(scenario_name)
    
    # Count packets per flow
    flow_counts = {}
    for p in packets:
        flow_counts[p.priority] = flow_counts.get(p.priority, 0) + 1
    
    print(f"\n   Total packets: {len(packets)}")
    print(f"   Queue capacity: {queue_size}")
    for fid in sorted(flow_counts.keys()):
        print(f"   Flow {fid}: {flow_counts[fid]} packets")
    
    strategies = [
        ("FCFS", FCFSQueue(max_queue_size=queue_size)),
        ("Fair Queue", FairQueue(max_queue_size=queue_size)),
        ("LAS Queue", LASQueue(max_queue_size=queue_size))
    ]
    
    results = {}
    
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
        results[name] = metrics
        
        print(f"\n   {name}:")
        print(f"      Processed:     {metrics['total_packets']} packets")
        print(f"      Dropped:       {metrics['dropped_packets']} ({metrics['drop_rate']*100:.1f}%)")
        print(f"      Avg Latency:   {metrics['avg_latency']:.2f}s")
        print(f"      Flow Fairness: {metrics['flow_fairness_index']:.4f}")
        
        # Show per-flow drops
        if metrics['dropped_packets'] > 0:
            flow_drops = {}
            for p in strategy.dropped_packets:
                flow_drops[p.priority] = flow_drops.get(p.priority, 0) + 1
            
            print(f"      Drops by flow:")
            for fid in sorted(flow_counts.keys()):
                drops = flow_drops.get(fid, 0)
                pct = (drops / flow_counts[fid]) * 100
                print(f"         Flow {fid}: {drops}/{flow_counts[fid]} ({pct:.1f}%)")
    
    return results


def main():
    print("=" * 100)
    print("REALISTIC TRAFFIC SCENARIOS - PACKET DROPPING ANALYSIS")
    print("=" * 100)
    print("\nComparing FCFS, Fair Queue, and LAS Queue under realistic conditions")
    
    scenarios = [
        ("message_texting", 15),      # Small queue for messaging
        ("video_streaming", 25),       # Medium queue for streaming
        ("online_meeting", 30),        # Larger queue for real-time
        ("file_download", 20),         # Constrained queue to show starvation
        ("mice_and_elephants", 25),    # LAS-favorable scenario
    ]
    
    all_results = {}
    
    for scenario, queue_size in scenarios:
        print("\n" + "=" * 100)
        all_results[scenario] = run_scenario(scenario, queue_size)
    
    # Summary
    print("\n" + "=" * 100)
    print("SUMMARY: Flow Fairness Comparison Across Scenarios")
    print("=" * 100)
    print(f"\n{'Scenario':<25} {'FCFS':<15} {'Fair Queue':<15} {'LAS Queue':<15}")
    print("-" * 70)
    
    scenario_names = {
        "message_texting": "📱 Message Texting",
        "video_streaming": "📺 Video Streaming",
        "online_meeting": "💻 Online Meeting",
        "file_download": "📥 File Download",
        "mice_and_elephants": "🐘🐭 Mice & Elephants"
    }
    
    for scenario, queue_size in scenarios:
        results = all_results[scenario]
        fcfs = results["FCFS"]["flow_fairness_index"]
        fq = results["Fair Queue"]["flow_fairness_index"]
        las = results["LAS Queue"]["flow_fairness_index"]
        
        # Mark the best
        best = max(fcfs, fq, las)
        fcfs_str = f"{fcfs:.4f}" + (" ✓" if fcfs == best else "")
        fq_str = f"{fq:.4f}" + (" ✓" if fq == best else "")
        las_str = f"{las:.4f}" + (" ✓" if las == best else "")
        
        print(f"{scenario_names[scenario]:<25} {fcfs_str:<15} {fq_str:<15} {las_str:<15}")
    
    print("\n" + "=" * 100)
    print("KEY INSIGHTS:")
    print("=" * 100)
    print("""
✓ = Best flow fairness for that scenario

📱 Message Texting: Equal small flows → All strategies similar
📺 Video Streaming: Unequal bandwidth demand → FQ/LAS protect smaller stream  
💻 Online Meeting: Multiple real-time users → Fair distribution critical
📥 File Download: One aggressive flow → Shows starvation prevention

CONCLUSION:
- Fair Queue consistently provides the best flow fairness
- LAS Queue is a good middle-ground, protecting small flows
- FCFS can severely starve smaller flows when one flow dominates
""")
    print("=" * 100)


if __name__ == "__main__":
    main()
