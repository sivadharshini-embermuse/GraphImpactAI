import sys

#from compare_files import compare_files
#from change_summary import create_change_summary
from analyzer.comparison.compare_files import compare_files
from analyzer.comparison.change_summary import create_change_summary


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python test_comparison.py "
            "<original_repository> "
            "<modified_repository>"
        )
        sys.exit(1)

    original_repository = sys.argv[1]
    modified_repository = sys.argv[2]

    comparison_result = compare_files(
        original_repository,
        modified_repository
    )

    output_path = (
        "analyzer/data/outputs/comparison_summary.json"
    )

    summary = create_change_summary(
        comparison_result,
        output_path
    )

    print("\nRepository Comparison Completed\n")

    print(
        f"Added Files      : "
        f"{summary['summary']['addedFilesCount']}"
    )

    print(
        f"Deleted Files    : "
        f"{summary['summary']['deletedFilesCount']}"
    )

    print(
        f"Modified Files   : "
        f"{summary['summary']['modifiedFilesCount']}"
    )

    print(
        f"Unchanged Files  : "
        f"{summary['summary']['unchangedFilesCount']}"
    )

    print(
        f"\nReport saved to: {output_path}"
    )


if __name__ == "__main__":
    main()