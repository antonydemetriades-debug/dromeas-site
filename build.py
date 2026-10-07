#!/usr/bin/env python3
"""Builds the static site from src/*.md (needs pandoc). Run: python3 build.py"""
import datetime, pathlib, re, subprocess
ROOT = pathlib.Path(__file__).parent
UPDATED = "7 October 2026"   # the privacy policy's "last updated" date — change it when the policy changes
PAGES = {"index": "", "privacy": "privacy/", "delete-account": "delete-account/"}
NAV = [("Home", "/"), ("Privacy", "/privacy/"), ("Delete account", "/delete-account/")]

def front(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines())
    return meta, text[m.end():]

def page(name, out):
    meta, body = front((ROOT / "src" / f"{name}.md").read_text())
    body = body.replace("{{updated}}", UPDATED)
    html = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5"], input=body, capture_output=True, text=True, check=True).stdout
    here = "/" + out
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == here else ""}>{t}</a>' for t, h in NAV)
    hero = '<div class="hero"><img src="/assets/logo-light.png" class="logo-light" alt="Dromeas News"><img src="/assets/logo-dark.png" class="logo-dark" alt="Dromeas News"></div>' if meta.get("home") else ""
    title = meta["title"] if meta.get("home") else f'{meta["title"]} · Dromeas News'
    year = datetime.date.today().year
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta['description']}">
<link rel="icon" href="/assets/icon.png">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header><div class="wrap"><a href="/"><img src="/assets/logo-light.png" class="logo-light" alt="Dromeas News"><img src="/assets/logo-dark.png" class="logo-dark" alt="Dromeas News"></a><nav>{nav}</nav></div></header>
<main><div class="wrap">{hero}{html}</div></main>
<footer><div class="wrap">© {year} Dromeas News · <a href="/privacy/">Privacy</a> · <a href="/delete-account/">Delete account</a> · <a href="mailto:privacy@dromeasnews.com">privacy@dromeasnews.com</a></div></footer>
</body>
</html>
"""
    target = ROOT / out / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc)

for name, out in PAGES.items():
    page(name, out)
(ROOT / "404.html").write_text((ROOT / "index.html").read_text())
print("built", list(PAGES))
