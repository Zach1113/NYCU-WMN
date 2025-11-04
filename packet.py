"""
Packet class representing network packets for QoS simulation.
"""

class Packet:
    """
    Represents a network packet with various properties.
    
    Attributes:
        id: Unique identifier for the packet
        arrival_time: Time when packet arrives at the queue
        priority: Priority level (higher value = higher priority)
        size: Size of packet in bytes
        service_time: Time required to process the packet
    """
    
    def __init__(self, packet_id, arrival_time, priority=1, size=1000, service_time=1.0):
        """
        Initialize a new packet.
        
        Args:
            packet_id: Unique identifier
            arrival_time: Time of arrival
            priority: Priority level (default=1)
            size: Packet size in bytes (default=1000)
            service_time: Processing time in seconds (default=1.0)
        """
        self.id = packet_id
        self.arrival_time = arrival_time
        self.priority = priority
        self.size = size
        self.service_time = service_time
        self.start_time = None  # Time when processing starts
        self.finish_time = None  # Time when processing completes
    
    def set_start_time(self, time):
        """Set the time when packet processing starts."""
        self.start_time = time
    
    def set_finish_time(self, time):
        """Set the time when packet processing completes."""
        self.finish_time = time
    
    def get_latency(self):
        """
        Calculate total latency (waiting time + service time).
        
        Returns:
            Latency in seconds, or None if not yet completed
        """
        if self.finish_time is None:
            return None
        return self.finish_time - self.arrival_time
    
    def get_waiting_time(self):
        """
        Calculate waiting time (time before processing starts).
        
        Returns:
            Waiting time in seconds, or None if not yet started
        """
        if self.start_time is None:
            return None
        return self.start_time - self.arrival_time
    
    def __lt__(self, other):
        """
        Less than comparison for priority queue (higher priority = lower value in heap).
        """
        # Negate priority so higher priority comes first in min-heap
        if self.priority != other.priority:
            return self.priority > other.priority
        # If same priority, use arrival time (FCFS tie-breaking)
        return self.arrival_time < other.arrival_time
    
    def __repr__(self):
        return (f"Packet(id={self.id}, arrival={self.arrival_time:.2f}, "
                f"priority={self.priority}, size={self.size})")
