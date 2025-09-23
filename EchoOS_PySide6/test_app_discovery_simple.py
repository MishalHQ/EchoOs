#!/usr/bin/env python3
"""
Simple test script for application discovery with error handling
This script handles permission issues gracefully
"""

import sys
import os
import json
from pathlib import Path

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.app_discovery import AppDiscovery

def test_app_discovery_simple():
    """Test application discovery with better error handling"""
    print("🚀 EchoOS Application Discovery Test (Simple)")
    print("=" * 50)
    
    # Initialize app discovery
    print("📱 Initializing application discovery...")
    app_disc = AppDiscovery()
    
    # Discover applications with error handling
    print("🔍 Discovering applications on the system...")
    print("Note: Some directories may be inaccessible due to permissions.")
    print("This is normal and the system will continue with accessible directories.\n")
    
    try:
        discovered_apps = app_disc.discover_and_save("config/apps.json")
        
        if discovered_apps:
            print(f"✅ Discovery completed! Found {len(discovered_apps)} applications")
            
            # Show statistics
            categories = {}
            for app in discovered_apps:
                category = app.get("category", "unknown")
                categories[category] = categories.get(category, 0) + 1
            
            print("\n📊 Discovery Statistics:")
            print("-" * 30)
            for category, count in sorted(categories.items()):
                print(f"  {category}: {count} apps")
            
            # Show sample applications
            print(f"\n📋 Sample Applications (first 15):")
            print("-" * 40)
            for i, app in enumerate(discovered_apps[:15]):
                name = app.get("name", "Unknown")
                category = app.get("category", "unknown")
                exec_path = app.get("exec", "No path")
                aliases = app.get("aliases", [])
                
                print(f"  {i+1:2d}. {name}")
                print(f"      Category: {category}")
                print(f"      Path: {exec_path}")
                if aliases:
                    print(f"      Aliases: {', '.join(aliases[:3])}{'...' if len(aliases) > 3 else ''}")
                print()
            
            if len(discovered_apps) > 15:
                print(f"  ... and {len(discovered_apps) - 15} more applications")
            
            # Test voice command examples
            print("\n🎤 Voice Command Examples:")
            print("-" * 30)
            sample_apps = discovered_apps[:5]
            for app in sample_apps:
                name = app.get("name", "Unknown")
                print(f"  • Say 'open {name.lower()}' to launch {name}")
            
            print(f"\n  • Say 'open [any app name]' to launch any discovered app")
            print(f"  • Say 'close [app name]' to close specific applications")
            print(f"  • Say 'close all tabs' to close all applications")
            
            return discovered_apps
            
        else:
            print("❌ No applications discovered")
            print("   This might be due to:")
            print("   - Permission restrictions")
            print("   - Empty system")
            print("   - Discovery errors")
            return []
            
    except Exception as e:
        print(f"❌ Discovery failed with error: {e}")
        print("   This is likely due to permission restrictions on Windows.")
        print("   Try running as administrator for better results.")
        return []

def show_troubleshooting():
    """Show troubleshooting information"""
    print("\n🔧 Troubleshooting:")
    print("-" * 20)
    print("If discovery fails or finds few apps:")
    print("1. Run as administrator (Windows)")
    print("2. Check file permissions")
    print("3. Ensure applications are installed")
    print("4. Check Windows security settings")
    print("5. Try the main EchoOS application instead")

def main():
    """Main test function"""
    print("EchoOS Application Discovery Test")
    print("This test will discover applications on your system")
    print("with proper error handling for permission issues.\n")
    
    # Test app discovery
    apps = test_app_discovery_simple()
    
    if apps:
        print(f"\n🎉 Test completed successfully!")
        print(f"   Discovered {len(apps)} applications")
        print(f"   Apps saved to: config/apps.json")
        print(f"   You can now use voice commands in EchoOS!")
        
        # Show next steps
        print(f"\n📋 Next Steps:")
        print(f"   1. Launch EchoOS: python main.py")
        print(f"   2. Go to 'App Catalog' tab")
        print(f"   3. Click 'Discover All Apps' for comprehensive scan")
        print(f"   4. Use voice commands to launch apps")
        
    else:
        print(f"\n⚠️  Limited discovery results")
        print(f"   This is normal on Windows due to security restrictions")
        print(f"   The main EchoOS application will work better")
        
        show_troubleshooting()

if __name__ == "__main__":
    main()
