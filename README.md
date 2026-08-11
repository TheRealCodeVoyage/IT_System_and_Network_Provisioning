# ACIT 4640 — IT Systems and Network Provisioning

Labs and flipped-material readings for BCIT's ACIT 4640, in the Computer Information Technology (CIT) diploma program. The course covers automated provisioning of IT infrastructure and application deployment, moving from manual system administration to Infrastructure as Code across physical, virtual, and cloud environments.

**Published site:** https://therealcodevoyage.github.io/2026-fall-ITSNP/

## What is published here

| Published | Not published |
|---|---|
| 10 labs | Slides (`.pptx`) |
| 11 flipped-material readings | Quizzes (these contain answer keys) |
| Course overview and learning outcomes | Tests and exams |
| | Internal planning documents |

Everything in the second column is excluded by [`.gitignore`](.gitignore) and is never tracked by git, so it cannot reach GitHub even though it sits in the same folder locally.

## Repository layout

```
.
├── Week-01/ ... Week-12/     Working source of truth (labs, readings, and
│                             locally, the un-tracked slides and quizzes)
├── docs/                     The Jekyll site published by GitHub Pages
│   ├── _config.yml
│   ├── index.md              Homepage: labs index + flipped-material index
│   ├── labs/                 Generated — do not edit by hand
│   └── flipped-material/     Generated — do not edit by hand
├── scripts/
│   └── sync-docs.py          Regenerates docs/ from the Week-XX folders
└── .gitignore
```

## Editing workflow

Edit lab and reading files in their `Week-XX/` folder — those are the originals. The copies under `docs/labs/` and `docs/flipped-material/` are generated, so hand edits there get overwritten.

After any edit:

```bash
python3 scripts/sync-docs.py
git add -A
git commit -m "Update Lab 5"
git push
```

GitHub Pages rebuilds automatically, usually within a minute.

`sync-docs.py` publishes only the files listed explicitly at the top of the script — nothing is published by glob. It also refuses to run on any filename containing `quiz`, `test`, `exam`, `answer`, `solution`, or `midterm`, as a second line of defence behind `.gitignore`.

### Why generated pages are wrapped in `{% raw %}`

Several labs contain Packer `{{timestamp}}` and Ansible/Jinja `{{ variable }}` syntax. Jekyll's Liquid template engine evaluates that syntax — including inside fenced code blocks — and would silently render those examples as empty strings. The sync script wraps each page body in `{% raw %}` to disable Liquid while leaving Markdown rendering intact.

## GitHub Pages setup

One-time configuration after pushing:

1. **Settings → Pages → Build and deployment**
2. **Source:** Deploy from a branch
3. **Branch:** `main`, folder: **`/docs`**

If you name the repository something other than `2026-fall-ITSNP`, update `baseurl` in [`docs/_config.yml`](docs/_config.yml) to match — a mismatch makes the theme's CSS and all internal links 404.

## Before making the repository public

```bash
git status --ignored      # confirm quizzes/slides appear under "Ignored files"
git ls-files              # confirm no quiz, test, exam, or .pptx file is listed
```

## Local preview (optional)

```bash
cd docs
bundle exec jekyll serve
```

Requires Ruby and the `github-pages` gem.

## License

Course materials are released under the [MIT License](LICENSE).
