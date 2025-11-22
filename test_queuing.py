"""
Unit tests for QoS queuing strategies.

Run with: python -m pytest test_queuing.py -v
or simply: python test_queuing.py
"""

import unittest
from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue, FairQueue
from simulation import PacketGenerator, Simulator


class TestPacket(unittest.TestCase):
    """Test Packet class functionality."""
    
    def test_packet_creation(self):
        """Test basic packet creation."""
        p = Packet(1, 0.0, priority=2, size=1500, service_time=1.0)
        self.assertEqual(p.id, 1)
        self.assertEqual(p.arrival_time, 0.0)
        self.assertEqual(p.priority, 2)
        self.assertEqual(p.size, 1500)
        self.assertEqual(p.service_time, 1.0)
    
    def test_packet_timing(self):
        """Test packet timing methods."""
        p = Packet(1, 0.0, priority=1, size=1000, service_time=1.0)
        self.assertIsNone(p.get_latency())
        self.assertIsNone(p.get_waiting_time())
        
        p.set_start_time(2.0)
        self.assertEqual(p.get_waiting_time(), 2.0)
        
        p.set_finish_time(3.0)
        self.assertEqual(p.get_latency(), 3.0)
    
    def test_packet_comparison(self):
        """Test packet priority comparison."""
        p1 = Packet(1, 0.0, priority=1)
        p2 = Packet(2, 0.0, priority=3)
        self.assertTrue(p2 < p1)  # Higher priority comes first


class TestFCFSQueue(unittest.TestCase):
    """Test FCFS queuing strategy."""
    
    def test_fcfs_order(self):
        """Test that FCFS processes packets in arrival order."""
        fcfs = FCFSQueue()
        p1 = Packet(1, 0.0, priority=1, service_time=1.0)
        p2 = Packet(2, 1.0, priority=3, service_time=1.0)
        p3 = Packet(3, 2.0, priority=2, service_time=1.0)
        
        fcfs.add_packet(p1)
        fcfs.add_packet(p2)
        fcfs.add_packet(p3)
        
        first = fcfs.process_next()
        self.assertEqual(first.id, 1)
        
        second = fcfs.process_next()
        self.assertEqual(second.id, 2)
        
        third = fcfs.process_next()
        self.assertEqual(third.id, 3)
    
    def test_fcfs_empty(self):
        """Test empty queue detection."""
        fcfs = FCFSQueue()
        self.assertTrue(fcfs.is_empty())
        
        fcfs.add_packet(Packet(1, 0.0))
        self.assertFalse(fcfs.is_empty())


class TestPriorityQueue(unittest.TestCase):
    """Test Priority Queue strategy."""
    
    def test_priority_order(self):
        """Test that Priority Queue processes high priority first."""
        pq = PriorityQueue()
        p1 = Packet(1, 0.0, priority=1, service_time=1.0)  # Low priority
        p2 = Packet(2, 1.0, priority=3, service_time=1.0)  # High priority
        p3 = Packet(3, 2.0, priority=2, service_time=1.0)  # Medium priority
        
        pq.add_packet(p1)
        pq.add_packet(p2)
        pq.add_packet(p3)
        
        # Should process in priority order: 3, 2, 1
        first = pq.process_next()
        self.assertEqual(first.priority, 3)
        
        second = pq.process_next()
        self.assertEqual(second.priority, 2)
        
        third = pq.process_next()
        self.assertEqual(third.priority, 1)


class TestRoundRobinQueue(unittest.TestCase):
    """Test Round-Robin queue strategy."""
    
    def test_round_robin_distribution(self):
        """Test that packets are distributed across queues."""
        rr = RoundRobinQueue(num_queues=3)
        
        # Add packets that should go to different queues
        p0 = Packet(0, 0.0, priority=1, service_time=1.0)  # Queue 0
        p1 = Packet(1, 1.0, priority=1, service_time=1.0)  # Queue 1
        p2 = Packet(2, 2.0, priority=1, service_time=1.0)  # Queue 2
        p3 = Packet(3, 3.0, priority=1, service_time=1.0)  # Queue 0 again
        
        rr.add_packet(p0)
        rr.add_packet(p1)
        rr.add_packet(p2)
        rr.add_packet(p3)
        
        # Verify distribution
        self.assertEqual(len(rr.queues[0]), 2)  # p0 and p3
        self.assertEqual(len(rr.queues[1]), 1)  # p1
        self.assertEqual(len(rr.queues[2]), 1)  # p2
    
    def test_round_robin_processing(self):
        """Test round-robin processing order."""
        rr = RoundRobinQueue(num_queues=2)
        
        p0 = Packet(0, 0.0, priority=1, service_time=1.0)
        p2 = Packet(2, 0.0, priority=1, service_time=1.0)
        p1 = Packet(1, 0.0, priority=1, service_time=1.0)
        p3 = Packet(3, 0.0, priority=1, service_time=1.0)
        
        rr.add_packet(p0)  # Queue 0
        rr.add_packet(p1)  # Queue 1
        rr.add_packet(p2)  # Queue 0
        rr.add_packet(p3)  # Queue 1
        
        # Should alternate between queues
        first = rr.process_next()
        self.assertEqual(first.id, 0)  # From queue 0
        
        second = rr.process_next()
        self.assertEqual(second.id, 1)  # From queue 1


class TestPacketGenerator(unittest.TestCase):
    """Test packet generation."""
    
    def test_packet_generation(self):
        """Test basic packet generation."""
        gen = PacketGenerator(seed=42)
        packets = gen.generate_packets(num_packets=10)
        
        self.assertEqual(len(packets), 10)
        self.assertTrue(all(isinstance(p, Packet) for p in packets))
    
    def test_priority_distribution(self):
        """Test that priority distribution is respected."""
        gen = PacketGenerator(seed=42)
        packets = gen.generate_packets(
            num_packets=100,
            priority_distribution={1: 1.0, 2: 0.0, 3: 0.0}
        )
        
        # All packets should have priority 1
        self.assertTrue(all(p.priority == 1 for p in packets))


class TestSimulator(unittest.TestCase):
    """Test simulation framework."""
    
    def test_basic_simulation(self):
        """Test basic simulation run."""
        fcfs = FCFSQueue()
        sim = Simulator(fcfs)
        
        packets = [
            Packet(1, 0.0, priority=1, service_time=1.0),
            Packet(2, 1.0, priority=1, service_time=1.0),
            Packet(3, 2.0, priority=1, service_time=1.0)
        ]
        
        metrics = sim.run(packets)
        
        self.assertEqual(metrics['total_packets'], 3)
        self.assertGreater(metrics['throughput'], 0)
        self.assertGreater(metrics['avg_latency'], 0)
    
    def test_metrics_calculation(self):
        """Test that metrics are calculated correctly."""
        pq = PriorityQueue()
        sim = Simulator(pq)
        
        packets = [
            Packet(1, 0.0, priority=1, service_time=2.0),
            Packet(2, 0.0, priority=2, service_time=2.0)
        ]
        
        metrics = sim.run(packets)
        
        # Check that all expected metrics are present
        self.assertIn('avg_latency', metrics)
        self.assertIn('avg_waiting_time', metrics)
        self.assertIn('throughput', metrics)
        self.assertIn('total_packets', metrics)
        self.assertIn('fairness_index', metrics)


class TestFairQueue(unittest.TestCase):
    """Test Fair Queue strategy."""
    
    def test_fair_queue_flow_separation(self):
        """Test that Fair Queue separates packets by flow (priority)."""
        fq = FairQueue()
        
        # Add packets with different priorities (flows)
        p1 = Packet(1, 0.0, priority=1, service_time=1.0)
        p2 = Packet(2, 0.0, priority=2, service_time=1.0)
        p3 = Packet(3, 0.0, priority=1, service_time=1.0)
        
        fq.add_packet(p1)
        fq.add_packet(p2)
        fq.add_packet(p3)
        
        # Verify flows are separated
        self.assertEqual(len(fq.flow_queues), 2)  # Two flows (priority 1 and 2)
        self.assertEqual(len(fq.flow_queues[1]), 2)  # Two packets in flow 1
        self.assertEqual(len(fq.flow_queues[2]), 1)  # One packet in flow 2
    
    def test_fair_queue_virtual_time(self):
        """Test that Fair Queue uses virtual finish times correctly."""
        fq = FairQueue()
        
        # Add packets with same priority but different service times
        p1 = Packet(1, 0.0, priority=1, service_time=2.0)
        p2 = Packet(2, 0.0, priority=1, service_time=1.0)
        
        fq.add_packet(p1)
        fq.add_packet(p2)
        
        # Process first packet
        first = fq.process_next()
        self.assertEqual(first.id, 1)  # First in queue
        
        # Virtual time should have advanced
        self.assertGreater(fq.virtual_time, 0)
    
    def test_fair_queue_fairness(self):
        """Test that Fair Queue provides fairness across flows."""
        fq = FairQueue()
        
        # Create packets from different flows with varying service times
        packets = [
            Packet(1, 0.0, priority=1, service_time=1.0),
            Packet(2, 0.0, priority=2, service_time=2.0),
            Packet(3, 0.0, priority=1, service_time=1.0),
            Packet(4, 0.0, priority=2, service_time=2.0),
        ]
        
        for p in packets:
            fq.add_packet(p)
        
        # Process all packets and track order
        processed_order = []
        while not fq.is_empty():
            packet = fq.process_next()
            if packet:
                processed_order.append(packet.id)
        
        # Fair Queue should interleave flows fairly
        # We should see packets from both flows processed
        self.assertEqual(len(processed_order), 4)
    
    def test_fair_queue_empty(self):
        """Test empty queue detection."""
        fq = FairQueue()
        self.assertTrue(fq.is_empty())
        
        fq.add_packet(Packet(1, 0.0, priority=1))
        self.assertFalse(fq.is_empty())


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    run_tests()
