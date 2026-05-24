"""
DynamoDB Client - Session and conversation storage
"""
import boto3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class DynamoDBClient:
    """
    Client for managing conversation sessions and history in DynamoDB.

    ❓ PRACTICE QUESTION 1:
    DynamoDB vs RDS cho conversation storage:
    - DynamoDB: NoSQL, fast, scalable, pay-per-request
    - RDS: SQL, ACID, complex queries, fixed cost

    Với GeekBrain chatbot (1000 users, 10K conversations/day),
    cái nào cost-effective hơn?
    """

    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.sessions_table = os.getenv('DYNAMODB_SESSIONS_TABLE', 'geekbrain_sessions')
        self.conversations_table = os.getenv('DYNAMODB_CONVERSATIONS_TABLE', 'geekbrain_conversations')

        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.sessions = self.dynamodb.Table(self.sessions_table)
        self.conversations = self.dynamodb.Table(self.conversations_table)

    def create_session(self, session_id: str, user_id: str = 'anonymous') -> Dict[str, Any]:
        """
        Create a new conversation session.

        ❓ PRACTICE QUESTION 2:
        TTL được set = now + 24 hours.
        DynamoDB sẽ tự động xóa session sau 24h.
        Nhưng deletion không instant (có thể delay vài giờ).
        Có vấn đề gì không?
        """
        now = datetime.utcnow()
        ttl = int((now + timedelta(hours=24)).timestamp())

        item = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': now.isoformat(),
            'last_updated': now.isoformat(),
            'turn_count': 0,
            'status': 'active',
            'ttl': ttl
        }

        self.sessions.put_item(Item=item)
        return item

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session metadata."""
        try:
            response = self.sessions.get_item(Key={'session_id': session_id})
            return response.get('Item')
        except Exception as e:
            print(f"Error getting session: {e}")
            return None

    def update_session(self, session_id: str, turn_count: int):
        """Update session metadata after each turn."""
        try:
            self.sessions.update_item(
                Key={'session_id': session_id},
                UpdateExpression='SET last_updated = :updated, turn_count = :count',
                ExpressionAttributeValues={
                    ':updated': datetime.utcnow().isoformat(),
                    ':count': turn_count
                }
            )
        except Exception as e:
            print(f"Error updating session: {e}")

    def add_turn(self, session_id: str, turn_number: int, user_message: str,
                 bot_response: str, entities: List[str] = None, tools: List[str] = None) -> Dict[str, Any]:
        """
        Add a conversation turn to history.

        ❓ PRACTICE QUESTION 3:
        Mỗi turn được store riêng biệt với sort key = turn_number.
        Query "get last 5 turns" sẽ như thế nào?
        Hint: DynamoDB Query với ScanIndexForward=False và Limit=5
        """
        item = {
            'session_id': session_id,
            'turn_number': turn_number,
            'timestamp': datetime.utcnow().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'entities_mentioned': entities or [],
            'tools_called': tools or [],
            'metadata': {}
        }

        self.conversations.put_item(Item=item)
        return item

    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversation history for a session.

        ❓ PRACTICE QUESTION 4:
        Với limit=10, query trả về 10 turns gần nhất.
        Nhưng nếu conversation có 100 turns, có cần load hết không?
        Sliding window approach: chỉ keep N turns gần nhất trong context.
        N nên là bao nhiêu?
        """
        try:
            response = self.conversations.query(
                KeyConditionExpression='session_id = :sid',
                ExpressionAttributeValues={':sid': session_id},
                ScanIndexForward=False,  # Descending order (newest first)
                Limit=limit
            )

            # Reverse to get chronological order
            items = list(reversed(response.get('Items', [])))
            return items

        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def get_last_turn(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent turn."""
        history = self.get_conversation_history(session_id, limit=1)
        return history[0] if history else None

    def extract_entities_from_history(self, session_id: str, limit: int = 5) -> Dict[str, List[str]]:
        """
        Extract all entities mentioned in recent conversation.

        ❓ PRACTICE QUESTION 5:
        Entity tracking giúp resolve pronouns.
        Ví dụ: "PaymentGW" mentioned in Turn 1 → "it" in Turn 2 = PaymentGW

        Nhưng nếu nhiều services được mention:
        Turn 1: "PaymentGW had 3 incidents"
        Turn 2: "AuthSvc had 1 incident"
        Turn 3: "What is its current latency?"

        "its" refer to service nào? Cần entity salience tracking.
        """
        history = self.get_conversation_history(session_id, limit=limit)

        entities = {
            'services': [],
            'teams': [],
            'people': [],
            'dates': [],
            'incidents': []
        }

        for turn in history:
            for entity in turn.get('entities_mentioned', []):
                # Simple categorization (in production, use NER)
                if entity in ['PaymentGW', 'AuthSvc', 'OrderSvc', 'NotificationSvc', 'FraudDetector', 'ReportingSvc']:
                    if entity not in entities['services']:
                        entities['services'].append(entity)
                elif entity.startswith('INC-'):
                    if entity not in entities['incidents']:
                        entities['incidents'].append(entity)
                elif entity.startswith('Team '):
                    if entity not in entities['teams']:
                        entities['teams'].append(entity)
                # Add more categorization logic

        return entities


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 6:
    Test DynamoDB client locally:

    1. Create session
    2. Add multiple turns
    3. Retrieve history
    4. Extract entities

    Verify data in DynamoDB console.
    """
    import uuid

    print("Testing DynamoDB Client...\n")

    client = DynamoDBClient()

    # Create test session
    session_id = str(uuid.uuid4())
    print(f"Creating session: {session_id}")
    client.create_session(session_id, user_id='test-user')

    # Add turns
    print("\nAdding conversation turns...")
    client.add_turn(
        session_id=session_id,
        turn_number=1,
        user_message="Which service had highest cost in March?",
        bot_response="PaymentGW at $7,500",
        entities=['PaymentGW', 'March 2026'],
        tools=['query_costs']
    )

    client.add_turn(
        session_id=session_id,
        turn_number=2,
        user_message="What is its current latency?",
        bot_response="PaymentGW's current p99 latency is 185ms",
        entities=['PaymentGW'],
        tools=['get_service_metrics']
    )

    # Update session
    client.update_session(session_id, turn_count=2)

    # Retrieve history
    print("\nRetrieving conversation history...")
    history = client.get_conversation_history(session_id)
    for turn in history:
        print(f"\nTurn {turn['turn_number']}:")
        print(f"  User: {turn['user_message']}")
        print(f"  Bot: {turn['bot_response']}")
        print(f"  Entities: {turn['entities_mentioned']}")

    # Extract entities
    print("\nExtracting entities...")
    entities = client.extract_entities_from_history(session_id)
    print(f"Services mentioned: {entities['services']}")

    print("\n✓ DynamoDB client working!")
    print(f"\nCheck DynamoDB console to verify data:")
    print(f"  Session: {session_id}")
