# fttt.org.tw — Static clone instructions

This folder is intended to hold a static mirror of http://fttt.org.tw. The environment I ran in does not have `wget` installed, so I could not complete the mirror here. Below are exact steps you can run on your macOS machine (zsh) to create the static site copy.

## 1) Install wget (if you don't have it)
Homebrew (recommended):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install wget
```

## 2) Mirror the site into this directory
Run these commands from a terminal. They will create the static mirror under this project folder.

```bash
cd ~/Code/fttt
mkdir -p static-page
cd static-page
# Mirror the site, download images/CSS/JS, and convert links to local files
/usr/local/bin/wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --span-hosts --domains=fttt.org.tw -e robots=off http://fttt.org.tw
```

Notes:
- On some Homebrew installs `wget` path may be `/opt/homebrew/bin/wget` (Apple silicon). Replace the path accordingly or ensure `wget` is in your PATH.
- `--page-requisites` ensures images, CSS, fonts and JS referenced by pages are downloaded.
- `--convert-links` rewrites links to point to local files so you can browse offline.

## 3) Quick verification
After the mirror finishes:

```bash
# show top-level download folder (wget usually creates `fttt.org.tw` folder)
ls -la
# summary size
du -sh .
# serve locally
python3 -m http.server 8000
# then visit http://localhost:8000/fttt.org.tw/ (or the mirrored root) in your browser
```

## 4) Optional: reorganize assets
The default wget mirror preserves the site layout. If you want images in an `images/` folder and CSS/JS in `assets/`, I can:
- either create a script that moves files and rewrites links in HTML, or
- use a more advanced mirroring tool and re-run the mirror with different options.

Rewriting links is non-trivial and must be done carefully to avoid breaking relative paths. Tell me which you prefer and I will implement it.

## 5) If you'd like me to run the mirror for you
If you want me to attempt the mirror from this environment, I can try to install `wget` and run the command — give me permission and I will proceed. If you prefer to run commands locally, run the steps above.

---
If anything in the above should be adjusted (different target folder, exclude certain paths, or keep/discard query parameters), tell me and I'll update the instructions or scripts.
