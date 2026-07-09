# GitHub Releases setup — Guns Views

Complete guide to publish updates for the desktop app auto-updater.

## 1. Create the GitHub repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `guns-lol-views-bot`
3. Visibility: **Public** (required for free auto-update without tokens) or **Private** (needs `GH_TOKEN`)
4. Do **not** initialize with README if you already have local code
5. Push your project:

```powershell
cd "D:\Discord\Guns.lol Views Bot"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/zfusions/guns-lol-views-bot.git
git push -u origin main
```

## 2. Verify auto-update config

Already configured in `frontend/package.json`:

```json
"repository": {
  "url": "https://github.com/zfusions/guns-lol-views-bot.git"
},
"build": {
  "publish": [{
    "provider": "github",
    "owner": "zfusions",
    "repo": "guns-lol-views-bot"
  }]
}
```

The app version lives in the same file (`"version": "2.0.0"`). Bump this before every release.

## 3. Install GitHub CLI (one time)

Download: [https://cli.github.com/](https://cli.github.com/)

```powershell
gh auth login
```

Choose GitHub.com → HTTPS → login in browser.

## 4. Build a release

```powershell
cd "D:\Discord\Guns.lol Views Bot"

# Bump version in frontend/package.json first (e.g. 2.0.1)
# Update frontend/lib/changelog.ts and CHANGELOG.md

.\build.ps1
```

Build output:

```
dist/
  guns-views.exe          ← bootstrap launcher for users
  .guns-runtime/          ← full app payload
  release/
    Guns-Views-2.0.1-win.zip   ← update package
    latest.yml                  ← metadata for electron-updater
```

## 5. Publish to GitHub Releases

```powershell
.\scripts\publish-github-release.ps1 -Version 2.0.1 -Notes "Bug fixes and UI improvements"
```

This creates tag `v2.0.1` and uploads:
- `Guns-Views-2.0.1-win.zip`
- `latest.yml`

### Manual publish (without script)

1. Open [github.com/zfusions/guns-lol-views-bot/releases/new](https://github.com/zfusions/guns-lol-views-bot/releases/new)
2. Tag: `v2.0.1` (must match package.json version)
3. Title: `Guns Views 2.0.1`
4. Upload both files from `dist/release/`
5. Publish release

## 6. What users experience

1. App checks GitHub 5 seconds after launch
2. Popup appears if a newer version exists
3. User clicks **Update now**
4. Download runs in background with progress bar
5. App installs over the old files and restarts automatically

Manual check: footer button **Check for updates**.

Changelog: burger menu → **Changelog**.

## 7. Private repository

Set a GitHub token before launching the app:

```powershell
$env:GH_TOKEN = "ghp_your_token_here"
```

Token needs `repo` scope (classic) or Contents read access (fine-grained).

## 8. Release checklist

- [ ] Bump `frontend/package.json` version
- [ ] Update `frontend/lib/changelog.ts`
- [ ] Update `CHANGELOG.md`
- [ ] Run `.\build.ps1`
- [ ] Verify `dist/release/latest.yml` and zip exist
- [ ] Run `.\scripts\publish-github-release.ps1 -Version X.Y.Z`
- [ ] Test on an older installed build

## 9. GitHub profile README

Copy `docs/github-profile-README.md` into a **separate** repository:

1. Create repo named exactly `zfusions` (same as your username)
2. Add `README.md` with the profile content
3. It appears on [github.com/zfusions](https://github.com/zfusions)

Profile README repo is independent from `guns-lol-views-bot`.
