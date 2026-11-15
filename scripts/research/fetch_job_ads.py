"""Fetch open QA/SDET job ads from public Greenhouse, Lever and Ashby job-board APIs.

Used for the skills matrix coverage check (PROJECT_BRIEF.md, section 2, core idea 3).
Standard library only. Saves one JSON file per ad; ad text is NOT committed.

Usage:
    python3 scripts/research/fetch_job_ads.py OUT_DIR "greenhouse,boards" "lever,boards" "ashby,boards"
"""
import json, re, sys, html, urllib.request, pathlib
OUT = pathlib.Path(sys.argv[1])
TITLE = re.compile(r"\b(sdet|qa|quality|test|tester|testing)\b", re.I)
EXCL = re.compile(r"\b(manager|director|analyst|intern|vp|head)\b", re.I)
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "job-research-script"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)
def clean(t):
    t = html.unescape(html.unescape(t or ""))
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()
def save(src, co, title, loc, url, text):
    if not TITLE.search(title) or EXCL.search(title) or len(text) < 800: return
    if not re.search(r"\b(automat|python|pytest|selenium|playwright|sdet)", text, re.I): return
    slug = re.sub(r"\W+", "-", f"{co}-{title}")[:80].lower()
    (OUT / f"{slug}.json").write_text(json.dumps(dict(source=src, company=co, title=title, location=loc, url=url, text=text)))
    print(f"OK  {co:22} | {title[:60]:60} | {loc[:30]}")
for co in sys.argv[2].split(","):
    try:
        d = get(f"https://boards-api.greenhouse.io/v1/boards/{co}/jobs?content=true")
        for j in d.get("jobs", []):
            save("greenhouse", co, j["title"], (j.get("location") or {}).get("name",""), j["absolute_url"], clean(j.get("content")))
    except Exception as e: print("GH fail", co, e)
for co in sys.argv[3].split(","):
    try:
        for j in get(f"https://api.lever.co/v0/postings/{co}?mode=json"):
            text = clean(j.get("descriptionPlain","")) + " " + " ".join(clean(l.get("content","")) + " " + l.get("text","") for l in j.get("lists",[]))
            save("lever", co, j["text"], j.get("categories",{}).get("location",""), j["hostedUrl"], text)
    except Exception as e: print("LV fail", co, e)
for co in sys.argv[4].split(","):
    try:
        for j in get(f"https://api.ashbyhq.com/posting-api/job-board/{co}").get("jobs", []):
            save("ashby", co, j["title"], j.get("location",""), j.get("jobUrl",""), clean(j.get("descriptionHtml") or j.get("descriptionPlain")))
    except Exception as e: print("AB fail", co, e)
