import json
import sys
from converter import convertFromFormat1, convertFromFormat2


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    data1 = load_json("data-1.json")
    data2 = load_json("data-2.json")

    result1 = convertFromFormat1(data1)
    result2 = convertFromFormat2(data2)

    print("Converted from Format 1:")
    print(json.dumps(result1, indent=2))

    print("\nConverted from Format 2:")
    print(json.dumps(result2, indent=2))


if __name__ == "__main__":
    main()
