"""
Simulation framework for testing QoS queuing strategies.
"""

import random
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
        random.seed(seed)
        self.packet_counter = 0
    
    def generate_packets(self, num_packets, arrival_rate=1.0, 
                        priority_distribution=None, size_distribution=None,
                        service_time_range=(0.5, 2.0)):
        """
        Generate a stream of packets.
        
        Args:
            num_packets: Number of packets to generate
            arrival_rate: Average packets per time unit (for Poisson process)
            priority_distribution: Dict with priority levels and their probabilities
            size_distribution: Dict with size ranges and their probabilities
            service_time_range: Tuple (min, max) for service time
            
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
        current_time = 0.0
        
        for _ in range(num_packets):
            # Generate arrival time using exponential distribution (Poisson process)
            inter_arrival = random.expovariate(arrival_rate)
            current_time += inter_arrival
            
            # Select priority based on distribution
            priority = random.choices(
                list(priority_distribution.keys()),
                weights=list(priority_distribution.values())
            )[0]
            
            # Select size based on distribution
            size_range = random.choices(
                list(size_distribution.keys()),
                weights=list(size_distribution.values())
            )[0]
            size = random.randint(size_range[0], size_range[1])
            
            # Generate service time
            service_time = random.uniform(service_time_range[0], service_time_range[1])
            
            packet = Packet(
                packet_id=self.packet_counter,
                arrival_time=current_time,
                priority=priority,
                size=size,
                service_time=service_time
            )
            
            packets.append(packet)
            self.packet_counter += 1
        
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
        import copy
        packet_copies = [copy.copy(p) for p in packets]
        
        # Reset packet state
        for p in packet_copies:
            p.start_time = None
            p.finish_time = None
        
        simulator = Simulator(strategy)
        metrics = simulator.run(packet_copies)
        results[strategy.name] = metrics
    
    return results
