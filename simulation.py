"""
Simulation framework for testing QoS queuing strategies.
"""

import random
import copy
from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue


class PacketGenerator:
    """Generate packets with various properties for simulation."""
    
    def __init__(self, seed=42):
        """
        Initialize packet generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.rng = random.Random(seed)
        self.packet_counter = 0
    
    def generate_packets(self, num_packets, arrival_rate=1.0, 
                        priority_distribution=None, size_distribution=None,
                        service_time_range=(0.5, 2.0), traffic_model='bursty'):
        """
        Generate a stream of packets with realistic traffic patterns.
        
        Args:
            num_packets: Number of packets to generate
            arrival_rate: Average packets per time unit
            priority_distribution: Dict with priority levels and their probabilities
            size_distribution: Dict with size ranges and their probabilities
            service_time_range: Tuple (min, max) for service time
            traffic_model: 'bursty' (default, realistic) or 'poisson' (random)
            
        Returns:
            List of Packet objects
        """
        if priority_distribution is None:
            priority_distribution = {1: 0.5, 2: 0.3, 3: 0.2}  # Low, Medium, High
        
        if size_distribution is None:
            size_distribution = {
                (500, 1000): 0.3,    # Small packets
                (1000, 2000): 0.5,   # Medium packets
                (2000, 5000): 0.2    # Large packets
            }
        
        packets = []
        
        if traffic_model == 'poisson':
            # Original Poisson model (random arrivals)
            current_time = 0.0
            for _ in range(num_packets):
                inter_arrival = self.rng.expovariate(arrival_rate)
                current_time += inter_arrival
                
                priority = self.rng.choices(
                    list(priority_distribution.keys()),
                    weights=list(priority_distribution.values())
                )[0]
                
                size_range = self.rng.choices(
                    list(size_distribution.keys()),
                    weights=list(size_distribution.values())
                )[0]
                size = self.rng.randint(size_range[0], size_range[1])
                service_time = self.rng.uniform(service_time_range[0], service_time_range[1])
                
                packets.append(Packet(
                    packet_id=self.packet_counter,
                    arrival_time=current_time,
                    priority=priority,
                    size=size,
                    service_time=service_time
                ))
                self.packet_counter += 1
        
        else:  # 'bursty' model (realistic traffic)
            # Bursty traffic model: flows send packets in bursts
            # This better represents real-world traffic (video, downloads, web)
            
            # Determine how many packets each flow gets
            flow_packet_counts = {}
            for _ in range(num_packets):
                priority = self.rng.choices(
                    list(priority_distribution.keys()),
                    weights=list(priority_distribution.values())
                )[0]
                flow_packet_counts[priority] = flow_packet_counts.get(priority, 0) + 1
            
            # Generate bursts for each flow
            current_time = 0.0
            burst_interval = 1.0 / arrival_rate  # Time between bursts
            
            # Create bursts at different times
            for flow_id in sorted(flow_packet_counts.keys()):
                num_flow_packets = flow_packet_counts[flow_id]
                
                # Each flow sends packets in bursts
                # Number of bursts for this flow (1-3 bursts)
                num_bursts = min(3, max(1, num_flow_packets // 10))
                packets_per_burst = num_flow_packets // num_bursts
                remaining = num_flow_packets % num_bursts
                
                for burst_idx in range(num_bursts):
                    # Burst arrival time (flows start at slightly different times)
                    burst_time = current_time + (flow_id - 1) * 0.1
                    
                    # Number of packets in this burst
                    burst_size = packets_per_burst + (1 if burst_idx < remaining else 0)
                    
                    # Generate packets in this burst
                    for pkt_in_burst in range(burst_size):
                        # Small jitter within burst (packets arrive very close together)
                        jitter = self.rng.uniform(0, 0.05)
                        arrival_time = burst_time + jitter
                        
                        size_range = self.rng.choices(
                            list(size_distribution.keys()),
                            weights=list(size_distribution.values())
                        )[0]
                        size = self.rng.randint(size_range[0], size_range[1])
                        service_time = self.rng.uniform(service_time_range[0], service_time_range[1])
                        
                        packets.append(Packet(
                            packet_id=self.packet_counter,
                            arrival_time=arrival_time,
                            priority=flow_id,
                            size=size,
                            service_time=service_time
                        ))
                        self.packet_counter += 1
                    
                    # Move to next burst time
                    current_time += burst_interval
        
        # Sort by arrival time
        packets.sort(key=lambda p: p.arrival_time)
        
        return packets


class Simulator:
    """Simulate packet processing with different queuing strategies."""
    
    def __init__(self, strategy):
        """
        Initialize simulator.
        
        Args:
            strategy: QueueingStrategy instance to simulate
        """
        self.strategy = strategy
    
    def run(self, packets):
        """
        Run simulation with given packets.
        
        Args:
            packets: List of Packet objects (should be sorted by arrival time)
            
        Returns:
            Dictionary of performance metrics
        """
        # Sort packets by arrival time
        packets = sorted(packets, key=lambda p: p.arrival_time)
        
        # Reset strategy state
        self.strategy.current_time = 0.0
        self.strategy.processed_packets = []
        
        # Add all packets to queue (in real system, they'd arrive over time)
        # For simulation purposes, we add them all at their arrival times
        packet_idx = 0
        
        while packet_idx < len(packets) or not self.strategy.is_empty():
            # Add packets that have arrived by current time
            while packet_idx < len(packets) and packets[packet_idx].arrival_time <= self.strategy.current_time:
                self.strategy.add_packet(packets[packet_idx])
                packet_idx += 1
            
            # Process next packet if queue is not empty
            if not self.strategy.is_empty():
                self.strategy.process_next()
            else:
                # If queue is empty, jump to next packet arrival
                if packet_idx < len(packets):
                    self.strategy.current_time = packets[packet_idx].arrival_time
        
        return self.strategy.get_metrics()


def run_experiment(packets, strategies):
    """
    Run experiment comparing multiple strategies.
    
    Args:
        packets: List of packets to process
        strategies: List of QueueingStrategy instances
        
    Returns:
        Dictionary mapping strategy name to metrics
    """
    results = {}
    
    for strategy in strategies:
        # Create a deep copy of packets for each strategy
        packet_copies = [copy.copy(p) for p in packets]
        
        # Reset packet state
        for p in packet_copies:
            p.start_time = None
            p.finish_time = None
        
        simulator = Simulator(strategy)
        metrics = simulator.run(packet_copies)
        results[strategy.name] = metrics
    
    return results
