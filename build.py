#!/usr/bin/env python3
"""Build script for creating the macOS application."""
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build_dirs():
    """Clean previous build directories."""
    print("🧹 Cleaning previous build directories...")
    dirs_to_clean = ["build", "dist", "YouTube Download.app"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            if dir_path.is_dir():
                shutil.rmtree(str(dir_path))
            else:
                dir_path.unlink()
            print(f"  ✓ Removed {dir_name}")


def create_app():
    """Create the macOS application bundle."""
    print("\n📦 Building macOS application...")

    # PyInstaller command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=YouTube Download",
        "--windowed",
        "--onefile",
        "--icon=assets/icon.icns" if Path("assets/icon.icns").exists() else "",
        "--add-data=src:src",
        "--hidden-import=PyQt6",
        "--hidden-import=yt_dlp",
        "--hidden-import=certifi",
        "--hidden-import=dotenv",
        "--osx-bundle-identifier=com.youtubedownload.app",
        "--noconfirm",
        "main.py"
    ]

    # Remove empty icon parameter if no icon exists
    cmd = [arg for arg in cmd if arg]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("  ✓ Application built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Build failed: {e}")
        print(e.stderr)
        return False


def create_dmg():
    """Create a DMG file for distribution (optional)."""
    if not shutil.which("hdiutil"):
        print("\n⚠️  hdiutil not found, skipping DMG creation")
        return

    print("\n💿 Creating DMG installer...")

    dmg_name = "YouTube Download.dmg"
    app_path = "dist/YouTube Download.app"

    if not Path(app_path).exists():
        print("  ✗ Application not found, cannot create DMG")
        return

    # Remove old DMG if exists
    if Path(dmg_name).exists():
        Path(dmg_name).unlink()

    cmd = [
        "hdiutil", "create",
        "-volname", "YouTube Download",
        "-srcfolder", "dist",
        "-ov", "-format", "UDZO",
        dmg_name
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✓ DMG created: {dmg_name}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ DMG creation failed: {e}")


def print_summary():
    """Print build summary."""
    print("\n" + "=" * 60)
    print("✨ Build Complete!")
    print("=" * 60)

    app_path = Path("dist/YouTube Download.app")
    dmg_path = Path("YouTube Download.dmg")

    if app_path.exists():
        size = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file())
        size_mb = size / (1024 * 1024)
        print(f"\n📱 Application: dist/YouTube Download.app ({size_mb:.1f} MB)")
        print("   To run: open 'dist/YouTube Download.app'")

    if dmg_path.exists():
        size_mb = dmg_path.stat().st_size / (1024 * 1024)
        print(f"\n💿 Installer: YouTube Download.dmg ({size_mb:.1f} MB)")
        print("   To distribute: Share 'YouTube Download.dmg'")

    print("\n📝 Notes:")
    print("   - The app includes all dependencies")
    print("   - FFmpeg must be installed separately on target system")
    print("   - First launch may be slow due to code signing verification")
    print("\n" + "=" * 60)


def main():
    """Main build process."""
    print("=" * 60)
    print("YouTube Download - Build Script")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Run this script from the project root.")
        sys.exit(1)

    # Clean previous builds
    clean_build_dirs()

    # Create the app
    if not create_app():
        sys.exit(1)

    # Optionally create DMG
    response = input("\n❓ Create DMG installer? (y/n): ").lower()
    if response == 'y':
        create_dmg()

    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
