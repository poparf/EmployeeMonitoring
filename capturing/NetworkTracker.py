# import asyncio
# import mitmproxy.http
# import pyshark
# import threading

# class FileDownloadInterceptor:
#     def __init__(self):
#         self.downloaded_files = []

#     def request(self, flow: mitmproxy.http.HTTPFlow):
#         """
#         Intercept and log details of HTTP requests potentially related to file downloads
#         """
#         # Check for potential file download requests
#         if any(ext in flow.request.path.lower() for ext in ['.zip', '.pdf', '.exe', '.tar', '.gz']):
#             print(f"\n[DOWNLOAD REQUEST]")
#             print(f"URL: {flow.request.pretty_url}")
#             print(f"Method: {flow.request.method}")
#             print(f"Headers: {dict(flow.request.headers)}")

#     def response(self, flow: mitmproxy.http.HTTPFlow):
#         """
#         Intercept and log details of HTTP responses potentially related to file downloads
#         """
#         # Check for potential file download responses
#         if flow.response and any(ext in flow.request.path.lower() for ext in ['.zip', '.pdf', '.exe', '.tar', '.gz']):
#             print(f"\n[DOWNLOAD RESPONSE]")
#             print(f"URL: {flow.request.pretty_url}")
#             print(f"Status Code: {flow.response.status_code}")
#             print(f"Content Type: {flow.response.headers.get('Content-Type', 'N/A')}")
#             print(f"Content Length: {flow.response.headers.get('Content-Length', 'N/A')}")

# def start_packet_capture():
#     """
#     Start Wireshark/Pyshark packet capture
#     """
#     # Capture on default network interface (modify as needed)
#     capture = pyshark.LiveCapture(interface='Wi-Fi')
    
#     print("\n[PYSHARK PACKET CAPTURE STARTED]")
    
#     for packet in capture.sniff_continuously(packet_count=100):
#         try:
#             # Filter for HTTP/HTTPS traffic
#             if 'HTTP' in packet or 'TLS' in packet:
#                 print("\n[PACKET CAPTURE]")
                
#                 # Print basic packet info
#                 if hasattr(packet, 'ip'):
#                     print(f"Source IP: {packet.ip.src}")
#                     print(f"Destination IP: {packet.ip.dst}")
                
#                 # Print protocol-specific details
#                 if hasattr(packet, 'http'):
#                     print("Protocol: HTTP")
#                     if hasattr(packet.http, 'request_method'):
#                         print(f"Method: {packet.http.request_method}")
#                     if hasattr(packet.http, 'host'):
#                         print(f"Host: {packet.http.host}")
                
#                 if hasattr(packet, 'tls'):
#                     print("Protocol: HTTPS")
#                     if hasattr(packet.tls, 'handshake_type'):
#                         print(f"TLS Handshake: {packet.tls.handshake_type}")
        
#         except Exception as e:
#             print(f"Error processing packet: {e}")

# def main():
#     # Start pyshark packet capture in a separate thread
#     packet_capture_thread = threading.Thread(target=start_packet_capture, daemon=True)
#     packet_capture_thread.start()

#     # Run mitmproxy interceptor
#     from mitmproxy.tools.main import mitmproxy
    
#     # Configure mitmproxy with our custom interceptor
#     mitmproxy([
#         '--mode', 'regular',
#         '--set', 'block_global=false',
#         '--scripts', __file__
#     ])

# if __name__ == '__main__':
#     print("Network Traffic Capture Script")
#     print("-----------------------------")
#     print("This script captures network traffic using mitmproxy and pyshark.")
#     print("Ensure you have the necessary dependencies installed:")
#     print("pip install mitmproxy pyshark")
#     print("\nRunning capture... (Press Ctrl+C to stop)\n")
    
#     main()

# # Note: 
# # 1. You may need to run this script with sudo/administrator privileges
# # 2. Modify the interface in start_packet_capture() as needed (e.g., 'en0' for Mac, 'eth0' for Linux)
# # 3. Configure your system's network proxy settings to use mitmproxy