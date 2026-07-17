#!/usr/bin/env python3
"""Refreshes repo/commit/star/follower counts inside dark_mode.svg and
light_mode.svg. Stdlib only. Expects GH_TOKEN in the environment."""
import json
import os
import re
import urllib.request

USER = 'Ultron011'
TOKEN = os.environ.get('GH_TOKEN', '')

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
}


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


user = get(f'https://api.github.com/users/{USER}')
repos = get(f'https://api.github.com/users/{USER}/repos?per_page=100')
commits = get(f'https://api.github.com/search/commits?q=author:{USER}&per_page=1')

stats = {
    'repos': str(user['public_repos']),
    'commits': f"{commits['total_count']:,}",
    'stars': str(sum(r['stargazers_count'] for r in repos)),
    'followers': str(user['followers']),
}

changed = False
for svg in ('dark_mode.svg', 'light_mode.svg'):
    text = open(svg, encoding='utf-8').read()
    for key, val in stats.items():
        pat = rf"('{key}'</tspan><tspan>: </tspan><tspan class=\"n\">)[\d,]+"
        text = re.sub(pat, rf'\g<1>{val}', text)
    changed |= text != open(svg, encoding='utf-8').read()
    open(svg, 'w', encoding='utf-8').write(text)

print('stats:', stats, '| svg changed:', changed)
