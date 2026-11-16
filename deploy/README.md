# Publishing the website

The website is built for GitHub Pages at `https://arshaduzzaman-sm.github.io/zero-to-sdet/`. It is **not published yet**. The repository stays private until Phase 9, and on the free plan GitHub Pages works only from a public repository.

`github-pages.yml` is the ready publish workflow. It sits here, outside `.github/workflows/`, so GitHub doesn't run it.

## What is already checked

- `bash scripts/check.sh` builds the site with `--strict`, so any warning fails.
- `scripts/check_built_site.py` serves the built `site/` folder at `/zero-to-sdet/`, the same path GitHub Pages uses, and opens every page and file. It fails on a broken link, a link that leaves the site's path, or a page that loads a script, style or image from another server.
- Diagrams use our own pinned copy of Mermaid, never `unpkg.com`. On its own, the theme would load Mermaid from `unpkg.com` (at whatever 12.x is newest) and every reader's browser would contact that server. `docs/assets/javascripts/mermaid-loader.js` stops that, and the browser checks the file's SHA-384 hash before running it. The big file loads only on pages that draw a diagram. The built-site check fails if any page lacks the loader or the hash doesn't match. Tested in Chrome with `unpkg.com` blocked: diagrams draw, pages without diagrams don't fetch the file, and a changed file is refused.
- Site address, repo link and "edit this page" link are set in `zensical.toml`.
- A 404 page is built. No file in the site starts with `_`, so nothing is hidden by GitHub.
- Share images use fonts kept in `docs/assets/fonts/`, so they build the same on GitHub's Linux machines.

## Switching it on (Phase 9, after the security audit)

Do these in order. Don't skip the first two.

1. Run the full security audit in `PROJECT_BRIEF.md` section 9, including a gitleaks scan of the **whole history**: `gitleaks detect --no-banner`.
2. Make the repository public: Settings, General, Danger Zone, Change visibility.
3. Settings, Pages, Build and deployment, Source: **GitHub Actions**.
4. Move the workflow into place, then run the pre-push checklist, commit and push:

    ```bash
    mkdir -p .github/workflows
    git mv deploy/github-pages.yml .github/workflows/pages.yml
    ```

5. Open the Actions tab and wait for "Publish website" to go green. Then open the site address above and check the home page, one lesson, search, dark mode and the 404 page.
6. Settings, Pages: tick **Enforce HTTPS** once GitHub offers it.

## Updating Mermaid

Pinned: Mermaid 12.2.0 from npm, MIT licence (`docs/assets/javascripts/vendor/mermaid-LICENSE.txt`). Stay on the major version the theme asks for (search the theme's `bundle.*.min.js` for `mermaid@`).

1. Pick a release at least two weeks old, with no open security advisory: <https://github.com/mermaid-js/mermaid/security/advisories>.
2. Download it from npm and check the tarball against npm's published `integrity` (sha512) before using it.
3. Copy `package/dist/mermaid.min.js` to `docs/assets/javascripts/vendor/mermaid-<version>.min.js`, and delete the old file (ask first).
4. In `mermaid-loader.js`, set `VERSION`, and set `INTEGRITY` to `sha384-` plus the output of `openssl dgst -sha384 -binary <file> | base64`.
5. Run `bash scripts/check.sh`, then open a page with a diagram in the preview.

## Keeping the workflow safe

- Actions are pinned to full commit SHAs. To update one, look up the new release's commit SHA on its GitHub page and change the SHA and the comment together. Never switch back to a plain tag like `@v5`.
- The workflow uses no secrets. If a later change seems to need one, stop and ask first.
