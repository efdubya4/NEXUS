#!/usr/bin/env python3
"""
Test script for NEXUS Guardian backend
"""

import requests
import json
import time

def test_guardian():
    """Test NEXUS Guardian functionality"""
    print("🧪 Testing NEXUS Guardian Backend...")
    
    # Test queries
    test_queries = [
        "How do I build a deck?",
        "Help me with Python programming",
        "What plants grow well in shade?",
        "How do I cook pasta?",
        "I need help with math homework"
    ]
    
    print("\n📝 Testing Guardian Processing:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        try:
            # Test direct Guardian processing
            from nexus_guardian import NexusGuardian
            guardian = NexusGuardian()
            result = guardian.process_query(query)
            
            response = result['payload']['response_text']
            domain = result['payload']['routing_decision']['domain']
            confidence = result['payload']['routing_decision']['confidence']
            response_time = result['payload']['performance_metrics']['response_time_ms']
            
            print(f"  ✅ Response: {response}")
            print(f"  🎯 Domain: {domain}")
            print(f"  📊 Confidence: {confidence:.2f}")
            print(f"  ⚡ Response Time: {response_time:.2f}ms")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n📊 Performance Metrics:")
    try:
        metrics = guardian.get_performance_metrics()
        print(f"  Total Queries: {metrics['metrics']['total_queries']}")
        print(f"  Successful Routes: {metrics['metrics']['successful_routes']}")
        print(f"  Average Response Time: {metrics['metrics']['average_response_time']:.2f}ms")
        print(f"  Efficiency Score: {metrics['efficiency_score']:.1f}%")
    except Exception as e:
        print(f"  ❌ Error getting metrics: {e}")

def test_api():
    """Test API endpoints"""
    print("\n🌐 Testing NEXUS API Endpoints...")
    
    base_url = "http://localhost:5001"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("  ✅ Health endpoint: OK")
        else:
            print(f"  ❌ Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Health endpoint error: {e}")
        return
    
    # Test query endpoint
    test_message = "How do I build a deck?"
    try:
        response = requests.post(
            f"{base_url}/api/nexus/query",
            json={"message": test_message}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("  ✅ Query endpoint: OK")
            print(f"  📝 Response: {data['response']}")
            print(f"  🎯 Domain: {data['routing']['domain']}")
            print(f"  📊 Confidence: {data['routing']['confidence']:.2f}")
        else:
            print(f"  ❌ Query endpoint: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Query endpoint error: {e}")
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/api/nexus/status")
        if response.status_code == 200:
            data = response.json()
            print("  ✅ Status endpoint: OK")
            print(f"  🏥 System Status: {data['status']}")
        else:
            print(f"  ❌ Status endpoint: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Status endpoint error: {e}")

if __name__ == "__main__":
    print("🚀 NEXUS AI Backend Test Suite")
    print("=" * 50)
    
    # Test Guardian directly
    test_guardian()
    
    # Test API endpoints
    test_api()
    
    print("\n✅ Backend testing complete!") 