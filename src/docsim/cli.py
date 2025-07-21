import argparse
import sys
from docsim.core import compare_folders

def main():
    parser = argparse.ArgumentParser(
        description="Compare document similarity between two folders"
    )
    parser.add_argument("folder1", help="First folder path")
    parser.add_argument("folder2", help="Second folder path")
    parser.add_argument("-t", "--threshold", type=float, default=0.85,
                      help="Similarity threshold (default: 0.85)")
    parser.add_argument("--csv", default="similarity_results.csv",
                      help="Output CSV filename")
    parser.add_argument("--html", default="similarity_dashboard.html",
                      help="Output HTML filename")
    parser.add_argument("-w", "--workers", type=int,
                      help="Number of parallel workers")

    args = parser.parse_args()
    
    try:
        compare_folders(
            args.folder1,
            args.folder2,
            similarity_threshold=args.threshold,
            output_csv=args.csv,
            output_html=args.html,
            max_workers=args.workers
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
