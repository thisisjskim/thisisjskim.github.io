# Validation of the initial website

- Built successfully with the GitHub Pages 232 dependency bundle and Jekyll 3.10.0, using strict front matter validation.
- Compiled upstream Academic Pages styling with Dart Sass 1.105.2. The generated CSS is committed so GitHub Pages' older Sass compiler is not needed for deployment.
- Checked 11 generated HTML pages for local links, image/script/stylesheet targets, duplicate IDs, heading anchors, page titles, required routes, and leftover sample or Notion-specific content.
- Migrated 6 paper notes containing 95 section headings and 52 local image references. All 52 image files decode successfully.
- Rendered 50 inline and 2 display equations with MathJax 3.2.2 without TeX errors. Checked that Markdown conversion preserves the math delimiters.
- Checked tables for unprocessed bold syntax and notes for unintended code blocks.
- Checked JavaScript syntax, including the MathJax configuration.

Browser screenshots, real-device layout, and interactions have not been visually tested in this execution environment. Responsive layout is implemented in CSS, but visual review on desktop and mobile remains useful. Original-paper links are external publisher/DOI links; the automated link checker validates local targets only.

Run the repeatable local target check after building:

```sh
python3 scripts/check_site.py _site
```
