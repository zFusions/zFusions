#!/usr/bin/env python3
"""Refresh public GitHub profile metrics in the terminal SVGs."""
import json
import os
import re
import urllib.request

USERNAME = "zFusions"
API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def get_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "zFusions-profile-updater"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def main():
    user = get_json(f"{API}/users/{USERNAME}")
    repos = []
    page = 1
    while True:
        batch = get_json(f"{API}/users/{USERNAME}/repos?per_page=100&page={page}&type=owner")
        if not batch:
            break
        repos.extend(batch)
        page += 1
    metrics = {
        "repo_data": str(user.get("public_repos", len(repos))),
        "star_data": str(sum(repo.get("stargazers_count", 0) for repo in repos)),
        "follower_data": str(user.get("followers", 0)),
        "fork_data": str(sum(repo.get("forks_count", 0) for repo in repos)),
    }
    for filename in ("dark_mode.svg", "light_mode.svg"):
        with open(filename, "r", encoding="utf-8") as file:
            svg = file.read()
        for element_id, value in metrics.items():
            svg = re.sub(
                rf'(<tspan id="{element_id}"[^>]*>).*?(</tspan>)',
                lambda match: match.group(1) + value + match.group(2),
                svg,
            )
        with open(filename, "w", encoding="utf-8") as file:
            file.write(svg)
    print("Updated profile metrics:", metrics)

if __name__ == "__main__":
    main()
