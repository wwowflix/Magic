import pandas as pd
import argparse


def normalize_youtube_trends(api_csv, autocomplete_csv, output_csv):
    print(f"📥 Loading: {api_csv}")
    api_df = pd.read_csv(api_csv)
    print("✅ API CSV loaded")

    api_df = api_df.rename(
        columns={"title": "keyword", "channelTitle": "author", "viewCount": "metric"}
    )
    api_df["platform"] = "YouTube"

    if "date" in api_df.columns:
        api_df["date"] = pd.to_datetime(api_df["date"], errors="coerce").dt.tz_localize(
            None
        )
    else:
        print("❌ 'date' column missing in API CSV")
        return

    api_df = api_df[["date", "keyword", "platform", "metric", "author"]]
    print("✅ API data cleaned")

    print(f"📥 Loading: {autocomplete_csv}")
    auto_df = pd.read_csv(autocomplete_csv)
    print("✅ Autocomplete CSV loaded")

    auto_df["author"] = auto_df.get("author", "")
    auto_df["date"] = pd.to_datetime(auto_df["date"], errors="coerce").dt.tz_localize(
        None
    )
    auto_df = auto_df[["date", "keyword", "platform", "metric", "author"]]
    print("✅ Autocomplete data cleaned")

    combined = pd.concat([api_df, auto_df], ignore_index=True)
    combined = combined.sort_values(by="date", ascending=False)

    combined.to_csv(output_csv, index=False, date_format="%Y-%m-%dT%H:%M:%SZ")
    print(f"✅ Normalized trends saved to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_csv", required=True)
    parser.add_argument("--auto_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    args = parser.parse_args()

    normalize_youtube_trends(args.api_csv, args.auto_csv, args.output_csv)
