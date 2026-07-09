# GST Circulars RSS Feed

An unofficial RSS feed for **CGST Circulars** published on the
[GST Council website](https://gstcouncil.gov.in/cgst-circulars).

The GST Council does not publish an RSS feed or an API for circulars.
This repo scrapes the circulars page and republishes it as valid RSS 2.0,
so it can be consumed by feed readers, Power Automate, Copilot Studio, n8n, etc.

## Feed URL

```
https://aashishsch.github.io/gst-circulars-feed/feed.xml
```

## How it works

| File | Purpose |
|---|---|
| `scrape.py` | Fetches the page, parses the circulars table, writes `docs/feed.xml` |
| `.github/workflows/build-feed.yml` | Re-runs the scraper twice daily and commits the result |
| `docs/feed.xml` | The generated RSS feed (served by GitHub Pages) |

## Run locally

```bash
pip install -r requirements.txt
python scrape.py
```

## Setup

1. Push this repo to GitHub.
2. **Settings → Pages** → Source: `main` branch, folder `/docs` → Save.
3. **Actions** tab → run **Build GST Circulars Feed** once manually.
4. Your feed is live at the URL above.

## Licence

Licensed under the [MIT License](LICENSE) — you are free to use, copy, modify
and distribute this code, including commercially, provided the copyright
notice is retained.

**Note on scope:** the MIT licence covers *this code only*. It does not grant
any rights over the circulars themselves, which are Government of India
publications, nor over the GST Council website's content.

## Acknowledgements

Inspired by [kskarthik/gstfeed](https://github.com/kskarthik/gstfeed), which
takes the same approach for the GST portal's News & Updates page. This repo is
an independent implementation targeting the GST Council's CGST Circulars page.

## Disclaimer

Unofficial. Not affiliated with the GST Council or the Government of India.
Scraping depends on the page's HTML structure; if the site is redesigned,
the scraper may need updating. Always verify against the official source
before relying on any circular for professional advice.

Provided "as is", without warranty of any kind. See [LICENSE](LICENSE).
