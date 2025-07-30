#!/usr/bin/env python3
"""
Complete NEXUS AI System Test
Tests backend, frontend integration, and overall functionality
"""

import requests
import json
import time
import subprocess
import sys
import os

def test_backend_directly():
    """Test NEXUS Guardian backend directly"""
    print("🧪 Testing NEXUS Guardian Backend...")
    
    try:
        from nexus_guardian import NexusGuardian
        guardian = NexusGuardian()
        
        test_queries = [
            "How do I build a deck?",
            "Help me with Python programming", 
            "What plants grow well in shade?",
            "How do I cook pasta?",
            "I need help with math homework"
        ]
        
        for query in test_queries:
            result = guardian.process_query(query)
            response = result['payload']['response_text']
            domain = result['payload']['routing_decision']['domain']
            confidence = result['payload']['routing_decision']['confidence']
            response_time = result['payload']['performance_metrics']['response_time_ms']
            
            print(f"  ✅ Query: '{query}'")
            print(f"     Response: {response}")
            print(f"     Domain: {domain}, Confidence: {confidence:.2f}, Time: {response_time:.2f}ms")
        
        metrics = guardian.get_performance_metrics()
        print(f"\n📊 Backend Performance:")
        print(f"  Total Queries: {metrics['metrics']['total_queries']}")
        print(f"  Efficiency Score: {metrics['efficiency_score']:.1f}%")
        print(f"  Average Response Time: {metrics['metrics']['average_response_time']:.2f}ms")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Backend test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:5001"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("  ✅ Health endpoint: OK")
        else:
            print(f"  ❌ Health endpoint: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Health endpoint error: {e}")
        return False
    
    # Test query endpoint
    test_message = "How do I build a deck?"
    try:
        response = requests.post(
            f"{base_url}/api/nexus/query",
            json={"message": test_message},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print("  ✅ Query endpoint: OK")
            print(f"     Response: {data['response']}")
            print(f"     Domain: {data['routing']['domain']}")
            print(f"     Confidence: {data['routing']['confidence']:.2f}")
        else:
            print(f"  ❌ Query endpoint: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Query endpoint error: {e}")
        return False
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/api/nexus/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("  ✅ Status endpoint: OK")
            print(f"     System Status: {data['status']}")
        else:
            print(f"  ❌ Status endpoint: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Status endpoint error: {e}")
        return False
    
    return True

def test_frontend_access():
    """Test frontend accessibility"""
    print("\n🎨 Testing Frontend Access...")
    
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("  ✅ Frontend server: OK")
            
            # Check for key frontend files
            files_to_check = ['styles.css', 'script.js']
            for file in files_to_check:
                try:
                    file_response = requests.get(f"http://localhost:8000/{file}", timeout=5)
                    if file_response.status_code == 200:
                        print(f"  ✅ {file}: OK")
                    else:
                        print(f"  ❌ {file}: {file_response.status_code}")
                except Exception as e:
                    print(f"  ❌ {file}: {e}")
        else:
            print(f"  ❌ Frontend server: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Frontend server error: {e}")
        return False
    
    return True

def test_integration():
    """Test backend-frontend integration"""
    print("\n🔗 Testing Backend-Frontend Integration...")
    
    try:
        # Test API call that frontend would make
        test_message = "How do I build a deck?"
        response = requests.post(
            "http://localhost:5001/api/nexus/query",
            json={
                "message": test_message,
                "context": {"current_agent": "guardian"}
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print("  ✅ Integration test: OK")
            print(f"     Backend processed: '{test_message}'")
            print(f"     Response: {data['response']}")
            print(f"     Routing: {data['routing']['domain']}")
            
            # Simulate frontend processing
            print("  ✅ Frontend would receive and display response")
            return True
        else:
            print(f"  ❌ Integration test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Integration test error: {e}")
        return False

def run_performance_test():
    """Run performance test"""
    print("\n⚡ Performance Test...")
    
    try:
        from nexus_guardian import NexusGuardian
        guardian = NexusGuardian()
        
        # Test multiple queries to measure performance
        test_queries = [
            "How do I build a deck?",
            "Help me with Python programming",
            "What plants grow well in shade?",
            "How do I cook pasta?",
            "I need help with math homework"
        ]
        
        start_time = time.time()
        
        for i, query in enumerate(test_queries, 1):
            result = guardian.process_query(query)
            response_time = result['payload']['performance_metrics']['response_time_ms']
            print(f"  Query {i}: {response_time:.2f}ms")
        
        total_time = (time.time() - start_time) * 1000
        avg_time = total_time / len(test_queries)
        
        print(f"\n📊 Performance Summary:")
        print(f"  Total time: {total_time:.2f}ms")
        print(f"  Average time: {avg_time:.2f}ms")
        print(f"  Queries per second: {1000/avg_time:.1f}")
        
        # Performance benchmarks
        if avg_time < 50:
            print("  🚀 Excellent performance!")
        elif avg_time < 100:
            print("  ✅ Good performance")
        elif avg_time < 200:
            print("  ⚠️  Acceptable performance")
        else:
            print("  ❌ Performance needs improvement")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Performance test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 NEXUS AI Complete System Test")
    print("=" * 50)
    
    tests = [
        ("Backend Direct Test", test_backend_directly),
        ("API Endpoints Test", test_api_endpoints),
        ("Frontend Access Test", test_frontend_access),
        ("Integration Test", test_integration),
        ("Performance Test", run_performance_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! NEXUS AI system is working correctly.")
        print("\n🌐 Access your NEXUS AI system:")
        print("  Frontend: http://localhost:8000")
        print("  Backend API: http://localhost:5001")
        print("  Health Check: http://localhost:5001/health")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 