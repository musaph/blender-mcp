from blender_mcp.server import main as server_main
import sys

def main():
    """Entry point for the blender-mcp package.
    
    Supports an optional --version flag to print version info.
    """
    if "--version" in sys.argv:
        from blender_mcp import __version__
        print(f"blender-mcp version {__version__}")
        return
    server_main()

if __name__ == "__main__":
    main()
