#!/usr/bin/env python3
"""
UDP Transceiver with Data Analysis
A comprehensive UDP client/server that can transmit and receive data
with built-in analysis capabilities for incoming data.
"""

import socket
import threading
import time
import json
import struct
import sys
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import argparse


class UDPDataAnalyzer:
    """Analyzes incoming UDP data and provides context."""
    
    def __init__(self):
        self.packet_count = 0
        self.total_bytes = 0
        self.data_types = {}
        self.start_time = datetime.now()
        self.last_packet_time = None
        
    def analyze_data(self, data: bytes, sender_addr: Tuple[str, int]) -> Dict[str, Any]:
        """Analyze incoming data and return analysis results."""
        self.packet_count += 1
        self.total_bytes += len(data)
        self.last_packet_time = datetime.now()
        
        analysis = {
            'timestamp': self.last_packet_time.isoformat(),
            'sender_ip': sender_addr[0],
            'sender_port': sender_addr[1],
            'packet_number': self.packet_count,
            'data_size': len(data),
            'total_bytes_received': self.total_bytes,
            'raw_data': data.hex(),
            'data_analysis': self._analyze_data_content(data)
        }
        
        return analysis
    
    def _analyze_data_content(self, data: bytes) -> Dict[str, Any]:
        """Analyze the content of the data."""
        analysis = {
            'length': len(data),
            'encoding_attempts': {},
            'possible_formats': []
        }
        
        # Try to decode as different text formats
        encodings = ['utf-8', 'ascii', 'latin-1']
        for encoding in encodings:
            try:
                decoded = data.decode(encoding)
                analysis['encoding_attempts'][encoding] = {
                    'success': True,
                    'content': decoded,
                    'printable_chars': sum(1 for c in decoded if c.isprintable())
                }
                if encoding == 'utf-8' and all(c.isprintable() or c.isspace() for c in decoded):
                    analysis['possible_formats'].append('text')
            except UnicodeDecodeError:
                analysis['encoding_attempts'][encoding] = {'success': False}
        
        # Try to parse as JSON
        try:
            if 'utf-8' in analysis['encoding_attempts'] and analysis['encoding_attempts']['utf-8']['success']:
                json_data = json.loads(analysis['encoding_attempts']['utf-8']['content'])
                analysis['possible_formats'].append('json')
                analysis['json_content'] = json_data
        except (json.JSONDecodeError, KeyError):
            pass
        
        # Check for common binary formats
        if len(data) >= 4:
            # Try to interpret as integers
            try:
                analysis['as_int32'] = struct.unpack('>I', data[:4])[0]  # Big-endian
                analysis['as_int32_le'] = struct.unpack('<I', data[:4])[0]  # Little-endian
            except struct.error:
                pass
        
        # Check if it looks like binary data
        non_printable = sum(1 for b in data if b < 32 or b > 126)
        if non_printable / len(data) > 0.3:
            analysis['possible_formats'].append('binary')
        
        return analysis
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics."""
        runtime = (datetime.now() - self.start_time).total_seconds()
        return {
            'runtime_seconds': runtime,
            'total_packets': self.packet_count,
            'total_bytes': self.total_bytes,
            'average_packet_size': self.total_bytes / self.packet_count if self.packet_count > 0 else 0,
            'packets_per_second': self.packet_count / runtime if runtime > 0 else 0,
            'last_packet_time': self.last_packet_time.isoformat() if self.last_packet_time else None
        }


class UDPTransceiver:
    """UDP client that can both send and receive data."""
    
    def __init__(self, target_ip: str, target_port: int, local_port: Optional[int] = None):
        self.target_ip = target_ip
        self.target_port = target_port
        self.local_port = local_port or target_port
        self.socket = None
        self.running = False
        self.analyzer = UDPDataAnalyzer()
        
    def start_receiver(self):
        """Start the UDP receiver in a separate thread."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', self.local_port))
            self.running = True
            
            print(f"UDP Receiver started on port {self.local_port}")
            print("Waiting for incoming data...")
            print("-" * 80)
            
            while self.running:
                try:
                    data, addr = self.socket.recvfrom(4096)  # Buffer size of 4KB
                    analysis = self.analyzer.analyze_data(data, addr)
                    self._print_analysis(analysis)
                    
                except socket.timeout:
                    continue
                except socket.error as e:
                    if self.running:  # Only print error if we're still supposed to be running
                        print(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"Error starting receiver: {e}")
        finally:
            if self.socket:
                self.socket.close()
    
    def _print_analysis(self, analysis: Dict[str, Any]):
        """Print formatted analysis of received data."""
        print(f"\n📦 Packet #{analysis['packet_number']} received at {analysis['timestamp']}")
        print(f"   From: {analysis['sender_ip']}:{analysis['sender_port']}")
        print(f"   Size: {analysis['data_size']} bytes")
        
        data_analysis = analysis['data_analysis']
        print(f"   Possible formats: {', '.join(data_analysis['possible_formats']) or 'Unknown'}")
        
        # Show text content if available
        if 'utf-8' in data_analysis['encoding_attempts'] and data_analysis['encoding_attempts']['utf-8']['success']:
            content = data_analysis['encoding_attempts']['utf-8']['content']
            print(f"   Text content: {repr(content)}")
            
        # Show JSON content if available
        if 'json_content' in data_analysis:
            print(f"   JSON data: {data_analysis['json_content']}")
            
        # Show binary representation for short data
        if analysis['data_size'] <= 32:
            print(f"   Hex: {analysis['raw_data']}")
            
        print("-" * 80)
    
    def send_data(self, data: str):
        """Send data to the target IP and port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Convert string to bytes
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            sock.sendto(data_bytes, (self.target_ip, self.target_port))
            print(f"✅ Sent {len(data_bytes)} bytes to {self.target_ip}:{self.target_port}")
            print(f"   Content: {repr(data)}")
            
        except Exception as e:
            print(f"❌ Error sending data: {e}")
        finally:
            sock.close()
    
    def send_json(self, json_data: Dict[str, Any]):
        """Send JSON data to the target."""
        json_string = json.dumps(json_data)
        self.send_data(json_string)
    
    def stop(self):
        """Stop the receiver."""
        self.running = False
        if self.socket:
            self.socket.close()
    
    def print_statistics(self):
        """Print current statistics."""
        stats = self.analyzer.get_statistics()
        print("\n📊 Statistics:")
        print(f"   Runtime: {stats['runtime_seconds']:.2f} seconds")
        print(f"   Total packets: {stats['total_packets']}")
        print(f"   Total bytes: {stats['total_bytes']}")
        print(f"   Average packet size: {stats['average_packet_size']:.2f} bytes")
        print(f"   Packets per second: {stats['packets_per_second']:.2f}")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='UDP Transceiver with Data Analysis')
    parser.add_argument('--ip', '-i', default='127.0.0.1', help='Target IP address (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=int, default=8888, help='Target port (default: 8888)')
    parser.add_argument('--local-port', '-l', type=int, help='Local port for receiving (default: same as target port)')
    parser.add_argument('--mode', '-m', choices=['send', 'receive', 'both'], default='both', 
                       help='Operation mode (default: both)')
    parser.add_argument('--message', '-msg', help='Message to send (for send mode)')
    
    args = parser.parse_args()
    
    transceiver = UDPTransceiver(args.ip, args.port, args.local_port)
    
    print(f"🚀 UDP Transceiver")
    print(f"   Target: {args.ip}:{args.port}")
    print(f"   Local port: {args.local_port or args.port}")
    print(f"   Mode: {args.mode}")
    print("=" * 80)
    
    try:
        if args.mode in ['receive', 'both']:
            # Start receiver in a separate thread
            receiver_thread = threading.Thread(target=transceiver.start_receiver, daemon=True)
            receiver_thread.start()
            time.sleep(0.5)  # Give receiver time to start
        
        if args.mode in ['send', 'both']:
            if args.message:
                # Send the provided message
                transceiver.send_data(args.message)
            else:
                # Interactive mode
                print("\n💬 Interactive mode - Type messages to send (or commands):")
                print("   Commands:")
                print("   - 'quit' or 'exit': Exit the program")
                print("   - 'stats': Show statistics")
                print("   - 'json:<data>': Send JSON data")
                print("   - Any other text: Send as UTF-8 text")
                print("-" * 80)
                
                while True:
                    try:
                        user_input = input("Enter message: ").strip()
                        
                        if user_input.lower() in ['quit', 'exit']:
                            break
                        elif user_input.lower() == 'stats':
                            transceiver.print_statistics()
                            continue
                        elif user_input.startswith('json:'):
                            try:
                                json_str = user_input[5:].strip()
                                json_data = json.loads(json_str)
                                transceiver.send_json(json_data)
                            except json.JSONDecodeError as e:
                                print(f"❌ Invalid JSON: {e}")
                            continue
                        elif user_input:
                            transceiver.send_data(user_input)
                            
                    except KeyboardInterrupt:
                        break
                    except EOFError:
                        break
        else:
            # Receive-only mode - wait for keyboard interrupt
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
    
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    
    finally:
        transceiver.stop()
        transceiver.print_statistics()
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()