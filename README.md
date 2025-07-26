# UDP Transceiver with Data Analysis

A comprehensive Python UDP communication tool that can transmit and receive UDP data from any IP address and port, with built-in data analysis capabilities for incoming data.

## Features

- **Bidirectional UDP Communication**: Send and receive UDP packets
- **Intelligent Data Analysis**: Automatically analyzes incoming data to determine:
  - Data format (text, JSON, binary)
  - Character encoding (UTF-8, ASCII, Latin-1)
  - Content interpretation
  - Statistical information
- **Flexible Operation Modes**: Send-only, receive-only, or both
- **Real-time Statistics**: Track packets, data rates, and timing
- **Interactive CLI**: Command-line interface with multiple options
- **Programmatic API**: Use as a Python library in your own code

## Files

- `udp_transceiver.py` - Main UDP transceiver script with CLI
- `udp_example.py` - Example usage and demonstrations
- `README.md` - This documentation

## Quick Start

### Command Line Usage

1. **Basic Usage (Both Send and Receive)**:
   ```bash
   python3 udp_transceiver.py --ip 192.168.1.100 --port 8888
   ```

2. **Receive Only Mode**:
   ```bash
   python3 udp_transceiver.py --mode receive --port 8888
   ```

3. **Send a Single Message**:
   ```bash
   python3 udp_transceiver.py --mode send --ip 192.168.1.100 --port 8888 --message "Hello UDP!"
   ```

4. **Use Different Local Port for Receiving**:
   ```bash
   python3 udp_transceiver.py --ip 192.168.1.100 --port 9999 --local-port 8888
   ```

### Interactive Mode

When running in interactive mode, you can use these commands:
- `quit` or `exit` - Exit the program
- `stats` - Show current statistics
- `json:{"key": "value"}` - Send JSON data
- Any other text - Send as UTF-8 text

### Example Interactive Session
```bash
$ python3 udp_transceiver.py --ip 127.0.0.1 --port 8888

🚀 UDP Transceiver
   Target: 127.0.0.1:8888
   Local port: 8888
   Mode: both
================================================================================
UDP Receiver started on port 8888
Waiting for incoming data...
--------------------------------------------------------------------------------

💬 Interactive mode - Type messages to send (or commands):
   Commands:
   - 'quit' or 'exit': Exit the program
   - 'stats': Show statistics
   - 'json:<data>': Send JSON data
   - Any other text: Send as UTF-8 text
--------------------------------------------------------------------------------
Enter message: Hello World!
✅ Sent 12 bytes to 127.0.0.1:8888
   Content: 'Hello World!'

📦 Packet #1 received at 2024-01-15T10:30:25.123456
   From: 127.0.0.1:54321
   Size: 12 bytes
   Possible formats: text
   Text content: 'Hello World!'
   Hex: 48656c6c6f20576f726c6421
--------------------------------------------------------------------------------
Enter message: json:{"temperature": 23.5, "humidity": 45}
✅ Sent 35 bytes to 127.0.0.1:8888
   Content: '{"temperature": 23.5, "humidity": 45}'

📦 Packet #2 received at 2024-01-15T10:30:30.654321
   From: 127.0.0.1:54322
   Size: 35 bytes
   Possible formats: text, json
   Text content: '{"temperature": 23.5, "humidity": 45}'
   JSON data: {'temperature': 23.5, 'humidity': 45}
--------------------------------------------------------------------------------
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--ip` | `-i` | Target IP address | 127.0.0.1 |
| `--port` | `-p` | Target port | 8888 |
| `--local-port` | `-l` | Local port for receiving | Same as target port |
| `--mode` | `-m` | Operation mode: send/receive/both | both |
| `--message` | `-msg` | Message to send (for send mode) | None |

## Programmatic Usage

You can also use the `UDPTransceiver` class in your own Python code:

```python
from udp_transceiver import UDPTransceiver
import threading
import time

# Create transceiver
transceiver = UDPTransceiver('192.168.1.100', 8888)

# Start receiver in background
receiver_thread = threading.Thread(target=transceiver.start_receiver, daemon=True)
receiver_thread.start()

# Send some data
transceiver.send_data("Hello from Python!")
transceiver.send_json({"message": "Hello", "timestamp": time.time()})

# Get statistics
stats = transceiver.analyzer.get_statistics()
print(f"Received {stats['total_packets']} packets")

# Stop when done
transceiver.stop()
```

## Data Analysis Features

The tool automatically analyzes incoming UDP data and provides:

### Text Analysis
- **Encoding Detection**: Attempts UTF-8, ASCII, and Latin-1 decoding
- **Printable Character Count**: Measures readability
- **Format Detection**: Identifies if data appears to be text

### JSON Analysis
- **JSON Parsing**: Automatically detects and parses valid JSON
- **Structure Display**: Shows parsed JSON structure

### Binary Analysis
- **Integer Interpretation**: Shows data as 32-bit integers (big and little endian)
- **Hex Representation**: Raw hexadecimal display
- **Binary Detection**: Identifies binary vs text data

### Statistical Analysis
- **Packet Counting**: Total packets received
- **Data Volume**: Total bytes transferred
- **Timing Information**: Timestamps and rates
- **Average Metrics**: Packet size, packets per second

## Example Output

When receiving data, the tool provides detailed analysis:

```
📦 Packet #3 received at 2024-01-15T10:30:25.123456
   From: 192.168.1.100:12345
   Size: 88 bytes
   Possible formats: text, json
   Text content: '{"sensor": "temperature", "value": 23.5, "unit": "celsius"}'
   JSON data: {'sensor': 'temperature', 'value': 23.5, 'unit': 'celsius'}
--------------------------------------------------------------------------------
```

## Use Cases

- **Network Testing**: Test UDP connectivity between devices
- **IoT Development**: Communicate with IoT devices using UDP
- **Protocol Development**: Analyze and debug custom UDP protocols
- **Data Monitoring**: Monitor UDP traffic and analyze data patterns
- **Sensor Networks**: Collect and analyze sensor data over UDP
- **Game Development**: Test UDP-based game networking
- **Real-time Applications**: Debug real-time UDP communications

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Examples

Run the example script to see various features in action:

```bash
python3 udp_example.py
```

This will demonstrate:
- Basic UDP communication
- Data analysis capabilities
- Different data types (text, JSON, binary)
- Statistics tracking

## Network Configuration

### Firewall Considerations
Make sure your firewall allows UDP traffic on the ports you're using:

```bash
# Linux (ufw)
sudo ufw allow 8888/udp

# Linux (iptables)
sudo iptables -A INPUT -p udp --dport 8888 -j ACCEPT
```

### Testing Locally
For local testing, use `127.0.0.1` (localhost) as the IP address.

### Remote Communication
For remote communication, ensure:
1. The target device is reachable
2. The target port is open and listening
3. No firewalls are blocking the communication
4. You have the correct IP address and port

## Troubleshooting

### Common Issues

1. **"Address already in use" error**:
   - Another process is using the port
   - Wait a few seconds and try again
   - Use a different port with `--local-port`

2. **"Permission denied" error**:
   - You might need elevated privileges for ports < 1024
   - Use ports > 1024 for regular users

3. **No data received**:
   - Check firewall settings
   - Verify the correct IP and port
   - Ensure the sender is actually sending data

4. **Connection refused**:
   - The target host is not listening on that port
   - Check if the target application is running

### Debug Tips

- Use `--mode receive` to only listen for incoming data
- Test locally first with `127.0.0.1`
- Check your network configuration
- Use network tools like `netstat` to verify port usage

## License

This project is open source. Feel free to modify and distribute according to your needs.