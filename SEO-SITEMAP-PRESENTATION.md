# Sitemap and robots presentation

## Executive summary

Two search-engine discovery files were added for **https://hotelrestaurantelite.ro/**:

- `sitemap.xml` lists the site's 18 public pages and connects each Romanian page to its English equivalent.
- `robots.txt` permits normal crawling and tells crawlers where the sitemap is located.

These files make the website easier for search engines to discover and understand. They do **not** guarantee indexing or improve rankings by themselves; page quality, technical health, authority, relevance, and performance still determine search visibility.

## What sitemap.xml does

A sitemap is a machine-readable inventory of canonical public URLs. It helps Google, Bing, and other compliant crawlers find pages even when a page has few inbound links.

This sitemap contains nine Romanian/English page pairs, for a total of 18 URLs:

| Romanian | English |
| --- | --- |
| `acasa.html` | `acasa-en.html` |
| `evenimente.html` | `evenimente-en.html` |
| `galerie.html` | `galerie-en.html` |
| `piscina.html` | `piscina-en.html` |
| `spa.html` | `spa-en.html` |
| `restaurant.html` | `restaurant-en.html` |
| `meniu.html` | `meniu-en.html` |
| `hotel.html` | `hotel-en.html` |
| `contact.html` | `contact-en.html` |

Each sitemap entry contains:

- `<loc>`: the full HTTPS address of the page.
- `hreflang="ro"`: the Romanian equivalent.
- `hreflang="en"`: the English equivalent.
- `hreflang="x-default"`: the Romanian version used as the default for unmatched languages.

Both versions contain reciprocal language references, which is required for reliable international targeting.

### Why no priority or changefreq?

Those values are frequently guessed and are not useful signals to Google. Omitting them keeps the sitemap accurate. A `lastmod` value was also omitted because it should reflect meaningful page-content changes and must be maintained reliably.

## What robots.txt does

The file contains:

```text
User-agent: *
Allow: /

Sitemap: https://hotelrestaurantelite.ro/sitemap.xml
```

This means:

1. The rules apply to every compliant crawler.
2. Crawling is allowed across the public site.
3. Crawlers are given the absolute sitemap address.

A robots file controls crawling, not guaranteed indexing. It should not be used to hide confidential material; private files require authentication or removal from the public server.

## Expected impact

The files can help with:

- Faster and more complete page discovery.
- Clearer understanding of the Romanian and English page relationships.
- Easier sitemap submission and diagnostics in search-engine webmaster tools.
- Reduced risk that an important page is overlooked because of weak internal linking.

They cannot directly guarantee:

- A particular Google ranking.
- That every submitted URL is indexed.
- Rich search results.
- Removal of duplicate content without matching canonical and hreflang tags in the HTML.

## Deployment and verification

After deployment, these addresses must return HTTP status 200:

- https://hotelrestaurantelite.ro/robots.txt
- https://hotelrestaurantelite.ro/sitemap.xml

Then:

1. Add and verify the domain in Google Search Console.
2. Submit `https://hotelrestaurantelite.ro/sitemap.xml` in the Sitemaps section.
3. Optionally submit the same sitemap in Bing Webmaster Tools.
4. Check indexing and language-targeting reports after crawlers revisit the site.

## If the domain changes

Replace every instance of `https://hotelrestaurantelite.ro/` in both files with the new canonical HTTPS origin. Then configure permanent HTTP 301 redirects from every old URL to its matching new URL, retain the old domain long enough for search engines and visitors to follow those redirects, and resubmit the sitemap under the new verified property.

## Recommended next SEO work

The most useful follow-up work is:

1. Add a canonical URL to every HTML page.
2. Add matching reciprocal `hreflang` tags directly inside every page's `<head>`.
3. Decide what the bare domain `https://hotelrestaurantelite.ro/` serves; ideally it should be the Romanian homepage or permanently redirect to `/acasa.html`.
4. Add unique title and meta-description content where missing.
5. Add Hotel, Restaurant, and LocalBusiness structured data with verified business details.
6. Compress large images and verify Core Web Vitals.
7. Add privacy/cookie documentation if analytics or non-essential cookies are introduced.

## Maintenance rule

Update the sitemap whenever a public indexable page is added, removed, renamed, translated, or moved to another domain. Do not add images, CSS, JavaScript, admin pages, redirects, errors, or duplicate URLs to this page sitemap.

