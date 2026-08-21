import argparse
import json

from laundry_care import LaundryCareWorkflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Laundry Care Agent — multi-agent Python prototype")
    parser.add_argument("request", nargs="*", help="Laundry-care request")
    parser.add_argument("--debug", action="store_true", help="Show the full agent trace")
    args = parser.parse_args()

    user_input = " ".join(args.request).strip()
    if not user_input:
        user_input = input("Describe your laundry-care question: ").strip()

    result = LaundryCareWorkflow().run(user_input)

    print("\nLaundry Care Agent")
    print("------------------")
    print(result.final_response)

    if args.debug:
        print("\nAgent trace")
        print("-----------")
        print(json.dumps(result.trace, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
