#!/usr/bin/env python3
"""Simple test runner for Phase 3 AlgoRewards"""

import subprocess
import sys
import os

def main():
    os.chdir('/Users/fundacionfuturo/AlgoReward/Algorand-Web3-Masterclasses-POC/AlgoRewards/projects/AlgoRewards-contracts')
    
    print("🧪 Running Phase 3 AlgoRewards Tests...")
    print("=" * 50)
    
    try:
        # Run the test script
        result = subprocess.run([
            'poetry', 'run', 'python', 'test_phase3.py'
        ], capture_output=True, text=True, check=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print("✅ Tests completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()