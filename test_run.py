"""
Test the photobooth application with a sample photo.
Run this to create a test photo and see the popup.
"""

import time
from pathlib import Path
from config_manager import ConfigManager

def test_photobooth():
    """Test the photobooth with a sample photo."""
    print("🧪 Testing Photobooth...")
    
    # Load config
    config = ConfigManager()
    watch_folder = Path(config.get("watch_folder"))
    
    print(f"📁 Watch folder: {watch_folder}")
    
    # Check if generate_sample.py exists
    if not Path("generate_sample.py").exists():
        print("❌ generate_sample.py not found!")
        print("Please make sure you have the sample photo generator.")
        return
    
    # Create test folder if needed
    watch_folder.mkdir(parents=True, exist_ok=True)
    
    print("\n🚀 Starting photobooth in test mode...")
    print("📸 In 3 seconds, a sample photo will be created...")
    print("   You should see a popup window appear!\n")
    
    # Start photobooth
    import photobooth
    
    # Wait a bit then generate sample
    time.sleep(3)
    
    import generate_sample
    sample_path = generate_sample.create_sample_photo(str(watch_folder))
    print(f"✅ Created test photo: {sample_path}")
    
    print("\n👀 Check for the popup window!")
    print("   (The photobooth is now running... Press Ctrl+C to stop)\n")

if __name__ == "__main__":
    test_photobooth()
