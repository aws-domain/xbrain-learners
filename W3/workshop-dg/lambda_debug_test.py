import socket
import urllib.request
import json

def lambda_handler(event, context):
    results = {}
    
    # Test 1: DNS resolution
    try:
        ip = socket.gethostbyname('httpbin.org')
        results['dns_resolution'] = f"OK — resolved to {ip}"
    except Exception as e:
        results['dns_resolution'] = f"FAIL — {str(e)}"
    
    # Test 2: TCP connect to port 443
    try:
        sock = socket.create_connection(('httpbin.org', 443), timeout=5)
        sock.close()
        results['tcp_connect_443'] = "OK — TCP handshake success"
    except Exception as e:
        results['tcp_connect_443'] = f"FAIL — {str(e)}"
    
    # Test 3: TCP connect to port 80 (HTTP)
    try:
        sock = socket.create_connection(('httpbin.org', 80), timeout=5)
        sock.close()
        results['tcp_connect_80'] = "OK — TCP handshake success"
    except Exception as e:
        results['tcp_connect_80'] = f"FAIL — {str(e)}"

    # Test 4: Reach AWS public endpoint (không cần internet, chỉ cần AWS network)
    try:
        sock = socket.create_connection(('s3.amazonaws.com', 443), timeout=5)
        sock.close()
        results['aws_s3_endpoint'] = "OK — reached S3 public endpoint"
    except Exception as e:
        results['aws_s3_endpoint'] = f"FAIL — {str(e)}"
    
    return {
        'statusCode': 200,
        'body': json.dumps(results, indent=2)
    }
