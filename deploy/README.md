# Publishing the website

The website is built for GitHub Pages at `https://arshaduzzaman-sm.github.io/zero-to-sdet/`. It is **not published yet**. The repository stays private until Phase 9, and on the free plan GitHub Pages works only from a public repository.

`github-pages.yml` is the ready publish workflow. It sits here, outside `.github/workflows/`, so GitHub doesn't run it.

## What is already checked

- `bash scripts/check.sh` builds the site with `--strict`, so any warning fails.
- `scripts/check_built_site.py` serves the built `site/` folder at `/zero-to-sdet/`, the same path GitHub Pages uses, and opens every page and file. It fails on a broken link, a link that leaves the site's path, or a page that loads a script, style or image from another server.
- Known gap: the theme's own script loads Mermaid (the diagram tool) from `unpkg.com` on pages with diagrams. That load starts inside a script, so the HTML check above can't see it. Waiting on the owner's decision about keeping a pinned copy on the site instead.
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

## Keeping the workflow safe

- Actions are pinned to full commit SHAs. To update one, look up the new release's commit SHA on its GitHub page and change the SHA and the comment together. Never switch back to a plain tag like `@v5`.
- The workflow uses no secrets. If a later change seems to need one, stop and ask first.
