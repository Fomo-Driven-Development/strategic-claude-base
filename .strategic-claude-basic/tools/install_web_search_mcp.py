#!/usr/bin/env python3
"""
Install web-search-mcp by checking requirements and extracting the zip file.
"""

import hashlib
import os
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from packaging import version

def check_command_version(command, min_version, version_flag="--version"):
    """Check if a command exists and meets minimum version requirement."""
    try:
        result = subprocess.run([command, version_flag], 
                              capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        # Extract version number (remove command name and 'v' prefix if present)
        if command == "node":
            # Node output: "v18.17.0" or "v20.5.0"
            version_str = output.replace('v', '')
        elif command == "npm":
            # NPM output: "8.19.2" or "9.8.1"
            version_str = output
        else:
            # Generic: try to find version pattern
            import re
            version_match = re.search(r'(\d+\.\d+\.\d+)', output)
            if version_match:
                version_str = version_match.group(1)
            else:
                return False, f"Could not parse version from: {output}"
        
        current_version = version.parse(version_str)
        required_version = version.parse(min_version)
        
        if current_version >= required_version:
            return True, f"{command} {version_str} ✅"
        else:
            return False, f"{command} {version_str} (requires {min_version}+) ❌"
            
    except subprocess.CalledProcessError:
        return False, f"{command} command failed ❌"
    except FileNotFoundError:
        return False, f"{command} not found ❌"
    except Exception as e:
        return False, f"{command} check failed: {e} ❌"

def check_requirements():
    """Check if Node.js and npm meet minimum version requirements."""
    print("Checking requirements...")
    
    requirements = [
        ("node", "18.0.0"),
        ("npm", "8.0.0")
    ]
    
    all_met = True
    for command, min_version in requirements:
        met, message = check_command_version(command, min_version)
        print(f"  {message}")
        if not met:
            all_met = False
    
    return all_met

def verify_file_hash(file_path, expected_hash):
    """Verify the SHA256 hash of a file."""
    print("🔍 Verifying file integrity...")
    
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        actual_hash = sha256_hash.hexdigest()
        if actual_hash == expected_hash:
            print("✅ File integrity verified")
            return True
        else:
            print("❌ Hash mismatch!")
            print(f"   Expected: {expected_hash}")
            print(f"   Actual:   {actual_hash}")
            return False
    except Exception as e:
        print(f"❌ Error verifying file hash: {e}")
        return False

def download_web_search_mcp(tools_dir):
    """Download the web-search-mcp release from GitHub."""
    url = "https://github.com/mrkrsl/web-search-mcp/releases/download/v0.3.2/web-search-mcp-v0.3.2.zip"
    zip_file = tools_dir / "web-search-mcp-v0.3.2.zip"
    
    # Check if file already exists
    if zip_file.exists():
        print(f"📁 {zip_file.name} already exists, verifying integrity...")
        expected_hash = "1d8a2aeeda4c927fe513aea6e2f8e5775ac661ec0a15b1cab4d6d617e48dd27e"
        if verify_file_hash(zip_file, expected_hash):
            print("📁 Existing file verified, skipping download")
            return True, zip_file
        else:
            print("❌ Existing file is corrupted, re-downloading...")
            zip_file.unlink()  # Remove the corrupted file
    
    print(f"📥 Downloading {url}...")
    
    try:
        # Create a request with headers to avoid some blocking
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (compatible; web-search-mcp-installer)'}
        )
        
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"❌ Download failed with status {response.status}")
                return False, None
            
            # Get file size for progress indication
            total_size = response.headers.get('content-length')
            if total_size:
                total_size = int(total_size)
                print(f"📊 File size: {total_size // 1024}KB")
            
            # Download with progress indication
            with open(zip_file, 'wb') as f:
                downloaded = 0
                chunk_size = 8192
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Show progress every 100KB
                    if total_size and downloaded % (100 * 1024) == 0:
                        progress = (downloaded / total_size) * 100
                        print(f"📊 Progress: {progress:.1f}%")
        
        print(f"✅ Downloaded {zip_file.name} successfully")
        
        # Verify file integrity
        expected_hash = "1d8a2aeeda4c927fe513aea6e2f8e5775ac661ec0a15b1cab4d6d617e48dd27e"
        if not verify_file_hash(zip_file, expected_hash):
            print("❌ File verification failed - removing corrupted download")
            zip_file.unlink()  # Remove the corrupted file
            return False, None
        
        return True, zip_file
        
    except urllib.error.URLError as e:
        print(f"❌ Download failed: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        return False, None

def run_npm_setup(extract_dir):
    """Run npm install and playwright install in the extracted directory."""
    # Check if setup already completed
    setup_marker = extract_dir / ".setup_complete"
    if setup_marker.exists():
        print("🔧 Setup already completed, skipping npm setup")
        return True
    
    print(f"📂 Changing to directory: {extract_dir.name}/")
    original_cwd = Path.cwd()
    
    try:
        # Change to extract directory
        os.chdir(extract_dir)
        
        # Step 1: npm install
        print("📥 Running npm install...")
        subprocess.run(["npm", "install"], 
                      capture_output=True, text=True, check=True)
        print("✅ npm install completed")
        
        # Step 2: npx playwright install
        print("🎭 Running npx playwright install...")
        subprocess.run(["npx", "playwright", "install"], 
                      capture_output=True, text=True, check=True)
        print("✅ Playwright browsers installed")
        
        # Verify that the main executable exists
        index_js = Path("dist/index.js")
        if not index_js.exists():
            print("❌ Critical file dist/index.js is missing!")
            return False
        
        print("✅ Installation verified - dist/index.js exists")
        
        # Create setup marker file
        setup_marker.touch()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e.cmd}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error during npm setup: {e}")
        return False
    finally:
        # Always return to original directory
        os.chdir(original_cwd)

def install_web_search_mcp(zip_file):
    """Install web-search-mcp by extracting the downloaded zip file."""
    tools_dir = Path(__file__).parent
    
    # Check if already extracted
    extract_dir = tools_dir / zip_file.stem
    if extract_dir.exists():
        print(f"📁 {extract_dir.name}/ already exists, skipping extraction")
        return True, extract_dir
    
    print(f"📦 Extracting {zip_file.name}...")
    extract_dir.mkdir(exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"✅ Extracted {zip_file.name} to {extract_dir.name}/")
        return True, extract_dir
        
    except zipfile.BadZipFile:
        print(f"❌ Error: {zip_file.name} is not a valid zip file")
        return False, None
    except Exception as e:
        print(f"❌ Error extracting {zip_file.name}: {e}")
        return False, None

def main():
    """Main installation process."""
    print("🔍 Web Search MCP Installer")
    print("=" * 40)
    
    # Check requirements first
    if not check_requirements():
        print("\n❌ Requirements not met!")
        print("\nPlease install:")
        print("  • Node.js 18.0.0 or higher: https://nodejs.org/")
        print("  • npm 8.0.0 or higher (usually comes with Node.js)")
        sys.exit(1)
    
    print("\n✅ All requirements met!")
    
    # Download the release
    tools_dir = Path(__file__).parent
    print("\n📥 Downloading web-search-mcp...")
    download_success, zip_file = download_web_search_mcp(tools_dir)
    
    if not download_success:
        print("\n❌ Download failed!")
        sys.exit(1)
    
    # Proceed with installation
    print("\n📦 Installing web-search-mcp...")
    success, extract_dir = install_web_search_mcp(zip_file)
    
    if not success:
        print("\n❌ Installation failed!")
        sys.exit(1)
    
    # Run npm setup after successful extraction
    print("\n🔧 Setting up npm dependencies...")
    if not run_npm_setup(extract_dir):
        print("\n❌ npm setup failed!")
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\nNext steps:")
    print("  • Configure the MCP server in your Claude Code settings")
    print("  • The web-search-mcp package is ready to use")
    if extract_dir:
        print(f"  • Location: {extract_dir.name}/")
    print("  • Refer to package.json for usage details")

if __name__ == "__main__":
    main()