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

## SEO foundation now implemented

In addition to the sitemap and robots file, the site now includes:

1. Self-referencing canonical URLs on all 18 HTML pages.
2. Reciprocal Romanian, English, and `x-default` `hreflang` annotations on every page.
3. Unique meta descriptions on all pages.
4. Open Graph and Twitter Card metadata using a dedicated 1200 × 630 sharing image.
5. `WebSite`, `Hotel`, `Restaurant`, and `DaySpa` JSON-LD on both language homepages.
6. WebP optimization for large images currently used by the website.
7. Lazy loading and asynchronous decoding for non-critical inline images.

The remaining deployment actions are to configure the bare domain to redirect permanently to `/acasa.html`, verify the live property in Google Search Console, submit the sitemap, and test representative URLs with PageSpeed Insights and the Rich Results Test. Add privacy and cookie documentation before introducing analytics or non-essential cookies.

## Maintenance rule

Update the sitemap whenever a public indexable page is added, removed, renamed, translated, or moved to another domain. Do not add images, CSS, JavaScript, admin pages, redirects, errors, or duplicate URLs to this page sitemap.
