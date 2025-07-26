#!/usr/bin/env python3
"""
Example usage of the UDP Transceiver
This demonstrates how to use the UDPTransceiver class programmatically.
"""

import time
import threading
import json
from udp_transceiver import UDPTransceiver


def example_basic_usage():
    """Basic example of sending and receiving UDP data."""
    print("=== Basic UDP Communication Example ===")
    
    # Create transceiver for localhost communication
    transceiver = UDPTransceiver('127.0.0.1', 8888)
    
    # Start receiver in background thread
    receiver_thread = threading.Thread(target=transceiver.start_receiver, daemon=True)
    receiver_thread.start()
    
    # Give receiver time to start
    time.sleep(1)
    
    # Send some test messages
    print("\nSending test messages...")
    transceiver.send_data("Hello, UDP World!")
    time.sleep(0.5)
    
    transceiver.send_data("This is a test message")
    time.sleep(0.5)
    
    # Send JSON data
    test_json = {
        "message": "Hello from JSON",
        "timestamp": time.time(),
        "data": [1, 2, 3, 4, 5]
    }
    transceiver.send_json(test_json)
    time.sleep(0.5)
    
    # Send some binary-looking data
    binary_data = bytes([0x01, 0x02, 0x03, 0x04, 0xFF, 0xFE])
    transceiver.send_data(binary_data)
    time.sleep(1)
    
    # Print statistics
    transceiver.print_statistics()
    
    # Stop the transceiver
    transceiver.stop()


def example_remote_communication():
    """Example of communicating with a remote host."""
    print("\n=== Remote Communication Example ===")
    print("Note: This requires a remote UDP server to be running")
    
    # Example for remote communication (adjust IP and port as needed)
    remote_ip = "192.168.1.100"  # Change this to your target IP
    remote_port = 9999           # Change this to your target port
    local_port = 8888           # Local port for receiving
    
    transceiver = UDPTransceiver(remote_ip, remote_port, local_port)
    
    print(f"Configured for remote communication:")
    print(f"  Target: {remote_ip}:{remote_port}")
    print(f"  Local port: {local_port}")
    
    # This would start the receiver and send data to the remote host
    # Uncomment the following lines if you have a remote UDP server:
    
    # receiver_thread = threading.Thread(target=transceiver.start_receiver, daemon=True)
    # receiver_thread.start()
    # time.sleep(1)
    # 
    # transceiver.send_data("Hello remote server!")
    # transceiver.send_json({"message": "Hello from Python client", "timestamp": time.time()})
    # 
    # time.sleep(5)  # Wait for potential responses
    # transceiver.print_statistics()
    # transceiver.stop()


def example_data_analysis():
    """Example showing the data analysis capabilities."""
    print("\n=== Data Analysis Example ===")
    
    transceiver = UDPTransceiver('127.0.0.1', 8889)
    
    # Start receiver
    receiver_thread = threading.Thread(target=transceiver.start_receiver, daemon=True)
    receiver_thread.start()
    time.sleep(1)
    
    print("\nSending various data types to demonstrate analysis...")
    
    # Text data
    transceiver.send_data("Plain text message")
    time.sleep(0.5)
    
    # JSON data
    json_data = {
        "type": "sensor_reading",
        "temperature": 23.5,
        "humidity": 45.2,
        "timestamp": time.time()
    }
    transceiver.send_json(json_data)
    time.sleep(0.5)
    
    # Unicode text
    transceiver.send_data("Hello 世界! 🌍")
    time.sleep(0.5)
    
    # Binary data that looks like an integer
    import struct
    binary_int = struct.pack('>I', 42)  # Big-endian 32-bit integer
    transceiver.send_data(binary_int)
    time.sleep(0.5)
    
    # Mixed binary data
    mixed_data = b'\x00\x01\x02\x03Hello\xFF\xFE'
    transceiver.send_data(mixed_data)
    time.sleep(1)
    
    transceiver.print_statistics()
    transceiver.stop()


if __name__ == "__main__":
    print("UDP Transceiver Examples")
    print("========================")
    
    try:
        # Run basic example
        example_basic_usage()
        
        # Show remote communication setup
        example_remote_communication()
        
        # Demonstrate data analysis
        example_data_analysis()
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    
    print("\nExamples completed!")