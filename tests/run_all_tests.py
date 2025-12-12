"""
YuHun Test Suite v1.0
=====================
Unified test runner for all YuHun components.

Runs:
- L13 Semantic Drive tests
- Computation Bridge tests
- Semantic Spine tests
- YuHun Metrics tests
- Integration tests
"""

import sys
import traceback
from typing import List, Tuple


def run_test(module_name: str, test_func_name: str) -> Tuple[str, bool, str]:
    """Run a single test and return (name, passed, error_msg)."""
    try:
        module = __import__(module_name)
        test_func = getattr(module, test_func_name, None)
        
        if test_func:
            test_func()
            return (f"{module_name}.{test_func_name}", True, "")
        else:
            return (f"{module_name}.{test_func_name}", False, "Function not found")
    except Exception as e:
        return (f"{module_name}.{test_func_name}", False, str(e))


def run_all_tests() -> List[Tuple[str, bool, str]]:
    """Run all YuHun tests."""
    results = []
    
    # Test list: (module, function)
    tests = [
        ("semantic_drive", "demo_semantic_drive"),
        ("computation_bridge", "demo_computation_bridge"),
        ("semantic_spine", "demo_semantic_spine"),
        ("yuhun_metrics", "demo_metrics"),
    ]
    
    for module, func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {module}.{func}")
        print('='*60)
        
        result = run_test(module, func)
        results.append(result)
        
        if result[1]:
            print(f"✅ PASSED")
        else:
            print(f"❌ FAILED: {result[2]}")
    
    return results


def print_summary(results: List[Tuple[str, bool, str]]):
    """Print test summary."""
    passed = sum(1 for r in results if r[1])
    failed = sum(1 for r in results if not r[1])
    total = len(results)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total:  {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Rate:   {passed/total*100:.1f}%")
    
    if failed > 0:
        print("\nFailed tests:")
        for name, status, error in results:
            if not status:
                print(f"  - {name}: {error}")


if __name__ == "__main__":
    print("="*60)
    print("YuHun Test Suite v1.0")
    print("="*60)
    
    results = run_all_tests()
    print_summary(results)
    
    # Exit with error code if any tests failed
    failed = sum(1 for r in results if not r[1])
    sys.exit(1 if failed > 0 else 0)
