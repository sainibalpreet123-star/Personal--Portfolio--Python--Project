"""
Personal Portfolio Generator (Python)
Mini Project - Data Mining (24SCT-307)

Reads profile.json, checks it, draws a skills chart with Pandas + Matplotlib and
renders a static website (site/index.html) using a Jinja2 template.

Run:    python build_portfolio.py
Open:   site/index.html   (or: cd site && python -m http.server 8000)
"""
import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

import matplotlib
matplotlib.use("Agg")                       # draw charts without opening a window
import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE = Path(__file__).resolve().parent
ALLOWED_SCHEMES = {"http", "https", "mailto"}
REQUIRED_FIELDS = ["name", "title", "tagline", "about", "contact", "skills", "projects", "education"]


# ----------------------------------------------------------------- step 1: load
def load_profile(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------- step 2: validate
def check_url(url, where):
    """Only web and e-mail links are allowed (blocks javascript: links)."""
    scheme = urlparse(url).scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"{where}: link '{url}' must start with http, https or mailto")


def validate_profile(p):
    """Raises ValueError for serious problems and returns a list of warnings."""
    warnings = []
    for key in REQUIRED_FIELDS:
        if key not in p or p[key] in ("", [], None):
            raise ValueError(f"profile.json: required field '{key}' is missing or empty")
    for s in p["skills"]:
        level = s.get("level")
        if not isinstance(level, (int, float)) or not 0 <= level <= 100:
            raise ValueError(f"skill '{s.get('name', '?')}': level must be a number from 0 to 100")
    for pr in p["projects"]:
        if pr.get("url"):
            check_url(pr["url"], f"project '{pr.get('title', '?')}'")
        else:
            warnings.append(f"project '{pr.get('title', '?')}' has no link")
    for link in p["contact"].get("links", []):
        check_url(link["url"], f"contact link '{link.get('label', '?')}'")
    if "@" not in p["contact"].get("email", ""):
        raise ValueError("contact.email must be an e-mail address")
    if "your" in p["contact"]["email"] or "[" in json.dumps(p):
        warnings.append("profile still contains placeholder text such as 'your.email' or '[Add ...]'")
    return warnings


# --------------------------------------------------------------- step 3: chart
def make_skill_chart(skills, out_file):
    df = pd.DataFrame(skills)
    df = df.sort_values(["category", "level"], ascending=[False, True]).reset_index(drop=True)
    palette = ["#1d5fa8", "#3b8de0", "#27ae60", "#e1a100", "#c0392b", "#8e44ad"]
    colors = {c: palette[i % len(palette)] for i, c in enumerate(sorted(df["category"].unique()))}
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(df) + 1.2))
    ax.barh(df["name"], df["level"], color=[colors[c] for c in df["category"]])
    for i, v in enumerate(df["level"]):
        ax.text(v + 1, i, f"{v:g}", va="center", fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Self-assessed level (0-100)")
    ax.set_title("Skills by category")
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[c]) for c in colors]
    ax.legend(handles, list(colors), loc="lower right", frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    return df


# ------------------------------------------------------------- step 4: render
def build_site(profile_path=BASE / "profile.json", out_dir=BASE / "site"):
    out_dir = Path(out_dir)
    profile = load_profile(profile_path)
    warnings = validate_profile(profile)

    (out_dir / "assets").mkdir(parents=True, exist_ok=True)
    df = make_skill_chart(profile["skills"], out_dir / "assets" / "skills.png")
    groups = [(cat, list(g["name"])) for cat, g in df.groupby("category", sort=True)]

    env = Environment(loader=FileSystemLoader(BASE / "templates"), autoescape=select_autoescape(["html"]))
    html = env.get_template("index.html").render(p=profile, groups=groups, year=datetime.date.today().year)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    shutil.copy(BASE / "static" / "style.css", out_dir / "style.css")
    return {"out": out_dir, "warnings": warnings, "skills": len(profile["skills"]),
            "projects": len(profile["projects"]), "bytes": len(html.encode("utf-8"))}


def main():
    ap = argparse.ArgumentParser(description="Build a personal portfolio website from profile.json")
    ap.add_argument("--profile", default=str(BASE / "profile.json"))
    ap.add_argument("--out", default=str(BASE / "site"))
    a = ap.parse_args()
    try:
        r = build_site(a.profile, a.out)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print("ERROR:", e)
        sys.exit(1)
    print(f"Portfolio built in: {r['out']}")
    print(f"Skills: {r['skills']} | Projects: {r['projects']} | HTML size: {r['bytes']} bytes")
    for w in r["warnings"]:
        print("Warning:", w)
    print("Open site/index.html in a browser to view the portfolio.")


if __name__ == "__main__":
    main()
