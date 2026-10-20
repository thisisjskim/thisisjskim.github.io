# Junseo Kim — Academic Website

Personal academic website at https://thisisjskim.github.io, based on [Academic Pages](https://github.com/academicpages/academicpages.github.io).

## Content

- `_pages/about.md`: introduction and research interests
- `_pages/cv.md`: CV
- `_paper_notes/`: Korean paper reading notes, with original-paper metadata
- `images/papers/`: local images used in the notes
- `_data/navigation.yml`: the three main navigation links
- `_config.yml`: site-wide configuration

## Local development

Install Ruby and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve
```

## Changing theme styles

The compiled `assets/css/main.css` is committed for compatibility with GitHub Pages. To regenerate it from the retained Academic Pages SCSS:

```sh
npm ci
npm run build:css
```

Custom design changes can usually be made in `assets/css/personal.css` without recompiling the theme.

## Publishing

GitHub Pages builds from `main` at the repository root. The Gemfile uses the GitHub Pages dependency bundle. Changes to `main` are published by GitHub Pages.

## Updating paper notes

Edit the Markdown file in `_paper_notes/`, keeping the front matter. Add images under `images/papers/<slug>/` and use root-relative paths. `paper_year` is the original publication year; `note_updated` is the note's revision date. Set `note_status: in-progress` for unfinished notes. Keep `note_toc` in sync with the explicit heading anchors.

Only reviewed content is copied from Notion; there is no automatic synchronization. Do not commit signed attachment URLs, private exports, or authentication information.

## Attribution

The theme's MIT license is retained in `LICENSE`. Paper figures and results belong to their original authors; each note links to the source paper. The notes are personal study records, not publications authored by the site owner.
