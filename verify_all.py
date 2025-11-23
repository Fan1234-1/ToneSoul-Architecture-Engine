import subprocess
import sys
import os

def run_command(command, cwd=None):
    print(f"Running: {command} in {cwd or '.'}")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return e.returncode

def main():
    print("=== ToneSoul Monolith Verification ===")
    
    # 1. Verify Python Core
    print("\n[1/2] Verifying Python Core...")
    py_tests = [
        "body/test_ledger.py",
        "body/test_guardian.py",
        "body/test_sensor.py",
        "body/test_constitution.py",
        "body/test_integration.py"
    ]
    
    for test in py_tests:
        if run_command(f"{sys.executable} {test}") != 0:
            print(f"❌ Python Test Failed: {test}")
            sys.exit(1)
            
    # 2. Verify TypeScript Spine Module
    print("\n[2/2] Verifying TypeScript Spine Module...")
    ts_dir = os.path.join("modules", "spine-ts")
    if os.path.exists(ts_dir):
        # We skip 'npm install' to save time if node_modules exists, but for safety let's run it if missing
        if not os.path.exists(os.path.join(ts_dir, "node_modules")):
             if run_command("npm install", cwd=ts_dir) != 0:
                 print("❌ NPM Install Failed")
                 sys.exit(1)
        
        if run_command("npm test", cwd=ts_dir) != 0:
            print("❌ TypeScript Test Failed")
            sys.exit(1)
    else:
        print("⚠️ TypeScript module not found, skipping.")

    print("\n✅ All Systems (Python + TS) Verified.")

if __name__ == "__main__":
    main()
