from spine_system import BasicKeywordSensor

def test_sensor():
    print("=== Testing NeuroSensor 2.0 ===")
    sensor = BasicKeywordSensor()

    # Test 1: Initial State
    print("\n--- Test 1: Initial State (No Context) ---")
    triad1 = sensor.estimate_triad("Apple")
    print(f"Input: 'Apple' | ΔS: {triad1.delta_s:.2f}")
    assert triad1.delta_s == 0.5 # Default neutral

    # Test 2: Context Continuity (Low Drift)
    print("\n--- Test 2: Context Continuity ---")
    # Context is now ["Apple"]
    # Input "Apple Pie" shares "Apple" (and chars), so similarity should be > 0, Drift < 1.0
    triad2 = sensor.estimate_triad("Apple Pie")
    print(f"Input: 'Apple Pie' (Context: Apple) | ΔS: {triad2.delta_s:.2f}")
    assert triad2.delta_s < 0.8 # Should have some similarity

    # Test 3: Context Drift (High Drift)
    print("\n--- Test 3: Context Drift ---")
    # Context is now ["Apple", "Apple Pie"]
    # Input "SpaceX Rocket" shares nothing
    triad3 = sensor.estimate_triad("SpaceX Rocket")
    print(f"Input: 'SpaceX Rocket' (Context: Apple Pie) | ΔS: {triad3.delta_s:.2f}")
    assert triad3.delta_s > 0.8 # High drift expected

    print("\n=== All Sensor Tests Passed ===")

if __name__ == "__main__":
    test_sensor()
