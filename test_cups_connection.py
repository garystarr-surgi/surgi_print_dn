#!/usr/bin/env python3
"""
Test script to diagnose CUPS connection issues
"""
import requests
import socket
import sys

def test_connection(host, port):
    """Test basic TCP connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Socket test failed: {e}")
        return False

def test_http(host, port):
    """Test HTTP access to CUPS"""
    try:
        url = f"http://{host}:{port}"
        response = requests.get(url, timeout=10)
        print(f"HTTP Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        return response.status_code == 200
    except Exception as e:
        print(f"HTTP test failed: {e}")
        return False

def test_ipp(host, port):
    """Test IPP access to CUPS"""
    try:
        url = f"http://{host}:{port}/ipp/print"
        headers = {'Content-Type': 'application/ipp'}
        response = requests.post(url, headers=headers, timeout=10)
        print(f"IPP Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"IPP test failed: {e}")
        return False

if __name__ == "__main__":
    host = "47.206.233.222"
    ports = [631, 80, 443]
    
    print(f"Testing CUPS server at {host}")
    print("=" * 50)
    
    for port in ports:
        print(f"\nTesting port {port}:")
        print("-" * 20)
        
        # Test TCP connection
        if test_connection(host, port):
            print(f"✅ TCP connection to {host}:{port} successful")
            
            # Test HTTP
            if test_http(host, port):
                print(f"✅ HTTP access to {host}:{port} successful")
            else:
                print(f"❌ HTTP access to {host}:{port} failed")
                
            # Test IPP (only on port 631)
            if port == 631:
                if test_ipp(host, port):
                    print(f"✅ IPP access to {host}:{port} successful")
                else:
                    print(f"❌ IPP access to {host}:{port} failed")
        else:
            print(f"❌ TCP connection to {host}:{port} failed")
    
    print("\n" + "=" * 50)
    print("Test complete!")
