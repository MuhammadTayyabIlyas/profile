"""Tell IndexNow search engines (Bing, which feeds ChatGPT search and Copilot, plus Yandex, Seznam, Naver)
that pages changed. Usage: python3 docs/indexnow.py URL [URL ...]   (no URLs = the main pages)."""
import json
import sys
import urllib.request

KEY = "6b85a28a1f5e7fb823694cdbad3c7d0a"
HOST = "tayyabcheema.com"
DEFAULT = ["/", "/teachingintheaiera", "/teachingintheaiera/read", "/teachingintheaiera/references",
           "/publications/", "/llms.txt", "/blog/"]


def main():
    urls = sys.argv[1:] or [f"https://{HOST}{p}" for p in DEFAULT]
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(r.status, r.reason, f"{len(urls)} URLs")


if __name__ == "__main__":
    main()
