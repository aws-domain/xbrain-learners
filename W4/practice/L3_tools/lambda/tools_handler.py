"""
Lambda Handler for GeekBrain Tools

This Lambda function handles tool calls from Bedrock Agent.
It provides access to:
1. Monitoring API (live metrics)
2. Database (historical data)
"""
import json
import os
import sqlite3
import urllib.request
import urllib.error
from typing import Dict, Any, List


# Configuration
MONITORING_API_URL = os.getenv('MONITORING_API_URL', 'http://localhost:8000')
DB_PATH = os.getenv('DB_PATH', '/tmp/geekbrain.db')


def get_service_metrics(service_name: str) -> Dict[str, Any]:
    """
    Get current metrics from monitoring API.

    ❓ PRACTICE QUESTION 1:
    Lambda function này gọi external API (monitoring_api).
    Trong production, API này sẽ ở đâu?
    - EC2 instance?
    - ECS container?
    - API Gateway + Lambda?
    Trade-offs của mỗi option?
    """
    try:
        url = f"{MONITORING_API_URL}/metrics/{service_name}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                'success': True,
                'service': service_name,
                'metrics': data
            }
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'error': f"Service not found: {service_name}",
            'status_code': e.code
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def query_costs(service: str = None, month: str = None) -> Dict[str, Any]:
    """
    Query monthly costs from database.

    ❓ PRACTICE QUESTION 2:
    Database file được mount vào Lambda tại /tmp/geekbrain.db.
    Nhưng /tmp trong Lambda có giới hạn 512MB và ephemeral.
    Trong production, nên dùng gì thay vì SQLite file?
    - RDS PostgreSQL?
    - DynamoDB?
    - Athena + S3?
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = "SELECT * FROM monthly_costs WHERE 1=1"
        params = []

        if service:
            query += " AND service = ?"
            params.append(service)

        if month:
            query += " AND month = ?"
            params.append(month)

        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        conn.close()

        return {
            'success': True,
            'count': len(results),
            'data': results
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def query_incidents(service: str = None, severity: str = None) -> Dict[str, Any]:
    """
    Query incident history from database.

    ❓ PRACTICE QUESTION 3:
    Function này return toàn bộ incident records.
    Nếu có 1000+ incidents, response sẽ rất lớn.
    Làm thế nào để optimize?
    - Pagination?
    - Limit results?
    - Aggregation?
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = "SELECT * FROM incidents WHERE 1=1"
        params = []

        if service:
            query += " AND service = ?"
            params.append(service)

        if severity:
            query += " AND severity = ?"
            params.append(severity)

        query += " ORDER BY date DESC"

        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        conn.close()

        return {
            'success': True,
            'count': len(results),
            'data': results
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def query_sla_targets(service: str) -> Dict[str, Any]:
    """
    Query SLA targets for a service.

    ❓ PRACTICE QUESTION 4:
    SLA targets ít khi thay đổi (static data).
    Có nên cache trong Lambda memory không?
    Lambda có persistent memory giữa invocations không?
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM sla_targets WHERE service = ?",
            (service,)
        )
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        conn.close()

        return {
            'success': True,
            'service': service,
            'targets': results
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def query_daily_metrics(service: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """
    Query historical daily metrics.

    ❓ PRACTICE QUESTION 5:
    Function này có thể return 90+ days of data (90 rows).
    Agent có cần tất cả data points không?
    Hay chỉ cần aggregated stats (avg, min, max)?
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = "SELECT * FROM daily_metrics WHERE service = ?"
        params = [service]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date"

        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        # Calculate summary stats
        if results:
            latencies = [r['latency_p99_ms'] for r in results]
            error_rates = [r['error_rate_percent'] for r in results]

            summary = {
                'avg_latency': sum(latencies) / len(latencies),
                'max_latency': max(latencies),
                'min_latency': min(latencies),
                'avg_error_rate': sum(error_rates) / len(error_rates),
                'max_error_rate': max(error_rates)
            }
        else:
            summary = {}

        conn.close()

        return {
            'success': True,
            'service': service,
            'count': len(results),
            'data': results,
            'summary': summary
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def lambda_handler(event, context):
    """
    Main Lambda handler for Bedrock Agent tool calls.

    Event structure from Bedrock Agent:
    {
        "actionGroup": "monitoring-tools",
        "apiPath": "/metrics/{service_name}",
        "httpMethod": "GET",
        "parameters": [...],
        "requestBody": {...}
    }

    ❓ PRACTICE QUESTION 6:
    Bedrock Agent gọi Lambda với specific event format.
    Làm thế nào để test Lambda locally mà không cần Agent?
    Hint: Tạo mock event và gọi handler trực tiếp.
    """
    print(f"Received event: {json.dumps(event)}")

    # Extract action details
    action_group = event.get('actionGroup', '')
    api_path = event.get('apiPath', '')
    http_method = event.get('httpMethod', 'GET')
    parameters = event.get('parameters', [])

    # Convert parameters list to dict
    params = {}
    for param in parameters:
        params[param['name']] = param['value']

    # Route to appropriate function
    try:
        if '/metrics/' in api_path:
            service_name = params.get('service_name')
            result = get_service_metrics(service_name)

        elif api_path == '/costs':
            result = query_costs(
                service=params.get('service'),
                month=params.get('month')
            )

        elif api_path == '/incidents':
            result = query_incidents(
                service=params.get('service'),
                severity=params.get('severity')
            )

        elif api_path == '/sla-targets':
            service = params.get('service')
            result = query_sla_targets(service)

        elif api_path == '/daily-metrics':
            result = query_daily_metrics(
                service=params.get('service'),
                start_date=params.get('start_date'),
                end_date=params.get('end_date')
            )

        else:
            result = {
                'success': False,
                'error': f"Unknown API path: {api_path}"
            }

    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }

    # Format response for Bedrock Agent
    response = {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': action_group,
            'apiPath': api_path,
            'httpMethod': http_method,
            'httpStatusCode': 200 if result.get('success') else 500,
            'responseBody': {
                'application/json': {
                    'body': json.dumps(result)
                }
            }
        }
    }

    return response


# For local testing
if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 7:
    Test Lambda locally trước khi deploy:

    1. Test get_service_metrics:
       python tools_handler.py test-metrics

    2. Test query_costs:
       python tools_handler.py test-costs

    3. Test full Lambda handler:
       python tools_handler.py test-handler
    """
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'test-metrics':
            print("Testing get_service_metrics...")
            result = get_service_metrics('PaymentGW')
            print(json.dumps(result, indent=2))

        elif command == 'test-costs':
            print("Testing query_costs...")
            result = query_costs(service='PaymentGW', month='2026-03')
            print(json.dumps(result, indent=2))

        elif command == 'test-handler':
            print("Testing lambda_handler...")
            mock_event = {
                'actionGroup': 'monitoring-tools',
                'apiPath': '/metrics/PaymentGW',
                'httpMethod': 'GET',
                'parameters': [
                    {'name': 'service_name', 'value': 'PaymentGW'}
                ]
            }
            result = lambda_handler(mock_event, None)
            print(json.dumps(result, indent=2))
    else:
        print("Usage: python tools_handler.py [test-metrics|test-costs|test-handler]")
