#!/usr/bin/env python3
"""
discover_integrations.py — Scan CAPABILITY.toml files across SuperInstance repos.

Builds a dependency graph, finds integration opportunities (crate A provides
what crate B requires), and outputs a markdown report.

Usage:
    python3 tools/discover_integrations.py /path/to/repos
    python3 tools/discover_integrations.py /path/to/repos --json

Requires: Python 3.11+ (tomllib) or the 'tomli' package (pip install tomli).
"""

import sys
import os
import json
from pathlib import Path
from collections import defaultdict

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        print("Error: Python 3.11+ required (for tomllib), or install 'tomli':",
              file=sys.stderr)
        print("  pip install tomli", file=sys.stderr)
        sys.exit(1)


def find_capability_files(root: Path) -> list:
    """Find all CAPABILITY.toml files in direct child directories."""
    results = []
    try:
        children = sorted(root.iterdir())
    except PermissionError:
        return results
    for child in children:
        cap = child / "CAPABILITY.toml"
        try:
            if cap.is_file():
                results.append(cap)
        except PermissionError:
            continue
    return results


def parse_capability(path: Path) -> dict:
    """Parse a CAPABILITY.toml file."""
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"  ⚠ Error parsing {path}: {e}", file=sys.stderr)
        return {}


def build_graph(caps):
    """Build dependency graph from parsed CAPABILITY.toml data."""
    graph = {
        "crates": {},
        "provides": defaultdict(list),
        "requires": defaultdict(list),
        "integrates": defaultdict(list),
    }

    for path, data in caps:
        if not data:
            continue
        crate_info = data.get("crate", {})
        name = crate_info.get("name", path.parent.name)
        graph["crates"][name] = {
            "path": str(path.parent),
            "layer": crate_info.get("layer", "unknown"),
            "description": crate_info.get("description", ""),
            "version": crate_info.get("version", "0.0.0"),
        }

        for cap in data.get("provides", {}).get("capabilities", []):
            graph["provides"][cap["name"]].append((name, cap))

        for req_type in ("required", "optional"):
            for req in data.get("requires", {}).get(req_type, []):
                graph["requires"][name].append((req["crate"], req))

        integrates = data.get("integrates", {})
        for intg_name, section in integrates.items():
            if isinstance(section, dict):
                target = section.get("crate", "")
                if target and target != "*":
                    graph["integrates"][name].append((target, section))

    return graph


def find_opportunities(graph):
    """Find integration opportunities: A requires B but no integration defined."""
    opportunities = []
    known = set()
    for crate_name, intgs in graph["integrates"].items():
        for target, _ in intgs:
            known.add((crate_name, target))
            known.add((target, crate_name))

    for crate_name, reqs in graph["requires"].items():
        for target_crate, req in reqs:
            if (crate_name, target_crate) not in known:
                opportunities.append({
                    "type": "missing_integration",
                    "crate": crate_name,
                    "target": target_crate,
                    "suggestion": (
                        f"{crate_name} requires {target_crate} "
                        f"({req.get('reason', 'no reason given')}) "
                        f"but no [integrates.*] section exists"
                    ),
                })

    return opportunities


def render_markdown(graph, opportunities):
    """Render the discovery report as markdown."""
    lines = ["# SuperInstance Integration Discovery Report\n"]
    lines.append(f"**Crates found:** {len(graph['crates'])}  ")
    lines.append(f"**Integration opportunities:** {len(opportunities)}\n")

    lines.append("## Crates by Layer\n")
    by_layer = defaultdict(list)
    for name, info in graph["crates"].items():
        by_layer[info["layer"]].append((name, info))
    for layer in sorted(by_layer):
        lines.append(f"### {layer.title()}\n")
        for name, info in sorted(by_layer[layer]):
            lines.append(f"- **{name}** v{info['version']} — {info['description']}")
        lines.append("")

    lines.append("## Integration Graph\n")
    for crate_name in sorted(graph["integrates"]):
        lines.append(f"### {crate_name}\n")
        for target, section in graph["integrates"][crate_name]:
            desc = section.get("description", "")
            lines.append(f"- → **{target}**: {desc}")
        lines.append("")

    if opportunities:
        lines.append("## Integration Opportunities\n")
        for opp in opportunities:
            lines.append(f"- 💡 {opp['suggestion']}")
        lines.append("")

    lines.append("## Capability Matrix\n")
    lines.append("| Capability | Provided By |")
    lines.append("|---|---|")
    for cap_name in sorted(graph["provides"]):
        providers = ", ".join(sorted(set(n for n, _ in graph["provides"][cap_name])))
        lines.append(f"| {cap_name} | {providers} |")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: discover_integrations.py <repos_dir> [--json]", file=sys.stderr)
        sys.exit(1)

    root = Path(sys.argv[1])
    json_output = "--json" in sys.argv

    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {root} for CAPABILITY.toml files...")
    cap_files = find_capability_files(root)
    print(f"Found {len(cap_files)} CAPABILITY.toml files\n")

    caps = []
    for path in cap_files:
        data = parse_capability(path)
        if data:
            name = data.get("crate", {}).get("name", path.parent.name)
            print(f"  ✓ {name}")
            caps.append((path, data))

    print(f"\nBuilding dependency graph...")
    graph = build_graph(caps)
    print(f"  {len(graph['crates'])} crates, "
          f"{sum(len(v) for v in graph['integrates'].values())} integrations")

    print("Finding integration opportunities...")
    opportunities = find_opportunities(graph)
    print(f"  {len(opportunities)} opportunities found\n")

    if json_output:
        output = {"graph": {}, "opportunities": opportunities}
        for k, v in graph.items():
            output["graph"][k] = dict(v) if isinstance(v, defaultdict) else v
        print(json.dumps(output, indent=2))
    else:
        print(render_markdown(graph, opportunities))


if __name__ == "__main__":
    main()
