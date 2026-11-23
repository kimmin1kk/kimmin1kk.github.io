"""옛 주소(kimmin1kk.github.io)의 모든 페이지를 blog.kimmin1.com으로 넘기는 정적 파일을 만든다.

새 블로그의 sitemap.xml에 있는 경로마다 index.html을 만들고, 그 안에서
같은 경로의 새 주소로 즉시 이동시킨다(meta refresh 0초 + canonical).
사이트맵에 없는 경로는 404.html이 자바스크립트로 같은 경로의 새 주소로 넘긴다.

사용법: python3 scripts/generate.py
"""
import html
import pathlib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NEW_ORIGIN = "https://blog.kimmin1.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent

PAGE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>블로그가 이사했습니다</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace({js_url} + location.search + location.hash);</script>
</head>
<body>
<p>블로그가 <a href="{url}">{url}</a>(으)로 옮겨졌습니다.</p>
</body>
</html>
"""

NOT_FOUND = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>블로그가 이사했습니다</title>
<script>location.replace("{origin}" + location.pathname + location.search + location.hash);</script>
</head>
<body>
<p>블로그가 <a href="{origin}/">{origin}</a>(으)로 옮겨졌습니다.</p>
</body>
</html>
"""


def main() -> None:
    # 기본 Python User-Agent는 Cloudflare 봇 차단에 걸려 403이 나므로 따로 지정한다
    req = urllib.request.Request(
        f"{NEW_ORIGIN}/sitemap.xml", headers={"User-Agent": "redirect-generator/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        tree = ET.fromstring(res.read())
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths = {"/"}
    for loc in tree.findall("s:url/s:loc", ns):
        url = loc.text.strip()
        if url.startswith(NEW_ORIGIN):
            paths.add(url[len(NEW_ORIGIN):] or "/")

    count = 0
    for path in sorted(paths):
        # 구글 사이트 인증 파일은 옛 주소의 Search Console 인증용이라 덮어쓰지 않는다
        if path.startswith("/google") and path.endswith(".html"):
            continue
        url = NEW_ORIGIN + path
        # 사이트맵의 한글 경로는 퍼센트 인코딩돼 있으므로 파일 경로는 디코딩해서 만든다
        rel = urllib.parse.unquote(path).lstrip("/")
        target = ROOT / rel / "index.html" if (not rel or rel.endswith("/")) else ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            PAGE.format(url=html.escape(url), js_url='"' + url.replace('"', "%22") + '"'),
            encoding="utf-8",
        )
        count += 1

    (ROOT / "404.html").write_text(NOT_FOUND.format(origin=NEW_ORIGIN), encoding="utf-8")
    print(f"{count} redirect pages + 404.html")


if __name__ == "__main__":
    main()
