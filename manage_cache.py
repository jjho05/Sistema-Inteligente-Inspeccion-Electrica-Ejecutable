"""
Utility script to manage embeddings cache.
Provides commands to view stats, clear cache, etc.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.rag.embeddings_cache import get_cache


def show_stats():
    """Show cache statistics."""
    cache = get_cache()
    stats = cache.get_stats()
    
    print("=== Embeddings Cache Statistics ===\n")
    print(f"Cached chunks: {stats['cached_chunks']}")
    print(f"Total size: {stats['total_size_mb']:.2f} MB")
    print(f"Cache directory: {stats['cache_dir']}")


def clear_cache():
    """Clear all cached embeddings."""
    cache = get_cache()
    
    print("=== Clear Embeddings Cache ===\n")
    stats = cache.get_stats()
    print(f"Current cache: {stats['cached_chunks']} chunks ({stats['total_size_mb']:.2f} MB)")
    
    response = input("\nAre you sure you want to clear the cache? (yes/no): ")
    if response.lower() == 'yes':
        cache.clear()
        print("\n✓ Cache cleared successfully")
    else:
        print("\n✗ Cache clear cancelled")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python3 manage_cache.py [stats|clear]")
        print("\nCommands:")
        print("  stats  - Show cache statistics")
        print("  clear  - Clear all cached embeddings")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'stats':
        show_stats()
    elif command == 'clear':
        clear_cache()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: stats, clear")
        sys.exit(1)


if __name__ == "__main__":
    main()
