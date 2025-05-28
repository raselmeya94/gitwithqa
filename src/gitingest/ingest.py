

import re
import asyncio
import inspect
import shutil
from pathlib import Path

from gitingest.clone import CloneConfig, clone_repo
from gitingest.ingest_from_query import ingest_from_query
from gitingest.parse_query import parse_query

def ingest(
    source: str,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    include_patterns: list[str] | str | None = None,
    exclude_patterns: list[str] | str | None = None,
    output_file: str | None = None,
) -> tuple[str, str, str]:

    query = None
    try:
        query = parse_query(
            source=source,
            max_file_size=max_file_size,
            from_web=False,
            include_patterns=include_patterns,
            ignore_patterns=exclude_patterns,
        )
        if query["url"]:
            clone_config = CloneConfig(
                url=query["url"],
                local_path=query["local_path"],
                commit=query.get("commit"),
                branch=query.get("branch"),
            )
            clone_result = clone_repo(clone_config)

            if inspect.iscoroutine(clone_result):
                asyncio.run(clone_result)
            else:
                # Optionally handle sync case if valid:
                # pass
                raise TypeError("clone_repo did not return a coroutine as expected.")

        summary, tree, content = ingest_from_query(query)

        if output_file:
            with open(output_file, "w") as f:
                f.write(tree + "\n" + content)
                

        return summary, tree, content

    finally:
        if query and query.get("url"):
            cleanup_path = Path(query["local_path"]).parents[1]
            if cleanup_path.exists() and cleanup_path.is_dir():
                shutil.rmtree(cleanup_path, ignore_errors=True)
