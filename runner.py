#!/usr/bin/env python3
"""
Start the main CTF Platform with responsive UI
"""

import subprocess
import sys
import os

def main():
    print("🐺 Starting Modern CTF Platform...")
    print("=" * 50)
    print("🌐 Main Platform: http://localhost:5000")
    print("📱 Responsive design for all devices")
    print("🎯 Features:")
    print("   - Responsive grid layout")
    print("   - White background with colored borders")
    print("   - Mobile-friendly design")
    print("   - Interactive challenge cards")
    print("   - Real-time leaderboard")
    print("=" * 50)
    print("Press Ctrl+C to stop the platform\n")
    
    try:
        # Run the main platform
        subprocess.run([sys.executable, "ctf_platform.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 CTF Platform stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting platform: {e}")
        print("Make sure Flask is installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
