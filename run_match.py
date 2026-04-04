from __future__ import annotations

import argparse

from cross_border_matcher import build_default_matcher_state, compute_cross_border_matches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find top cross-border municipality matches between Denmark and Sweden."
    )
    parser.add_argument(
        "--country",
        required=True,
        choices=("denmark", "sweden"),
        help="Source country",
    )
    parser.add_argument(
        "--municipality",
        required=True,
        help="Source municipality name",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of matches to return",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    matcher_state = build_default_matcher_state()
    matches = compute_cross_border_matches(
        source_country_id=args.country,
        source_municipality=args.municipality,
        matcher_state=matcher_state,
        top_n=args.top,
    )

    print(f"source_country={args.country}")
    print(f"source_municipality={args.municipality}")
    for index, match in enumerate(matches, start=1):
        print(
            f"{index}. {match.municipality} ({match.country_id}) | "
            f"score={match.score} | "
            f"similar={', '.join(match.similar_factors)} | "
            f"different={', '.join(match.different_factors)}"
        )


if __name__ == "__main__":
    main()
