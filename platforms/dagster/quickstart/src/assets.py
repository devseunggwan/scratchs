import json

import pandas as pd
import requests
from dagster import Config, MaterializeResult, MetadataValue, asset


class HNStoriesConfig(Config):
    top_stories_limit: int = 10
    hn_top_story_ids_path: str = "hackernews_top_story_ids.json"
    hn_top_stories_path: str = "hackernews_top_stories.json"


@asset
def hackernews_top_story_ids(config: HNStoriesConfig):
    top_story_ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()

    with open(config.hn_top_story_ids_path, "w") as f:
        json.dump(top_story_ids[: config.top_stories_limit], f)


@asset(deps=[hackernews_top_story_ids])
def hackernews_top_stories(config: HNStoriesConfig) -> MaterializeResult:
    with open(config.hn_top_story_ids_path, "r") as f:
        hackernews_top_story_ids = json.load(f)

        results = []
        for item_id in hackernews_top_story_ids:
            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            ).json()
            results.append(item)

        df = pd.DataFrame(results)
        df.to_csv(config.hn_top_stories_path)

        return MaterializeResult(
            metadata={
                "num_records": len(df),
                "preview": MetadataValue.md(
                    str(df[["title", "by", "url"]].to_markdown())
                ),
            }
        )
