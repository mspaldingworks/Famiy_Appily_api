# Pushing these commits

I staged and committed everything, but I can't push — I have no credentials for your GitHub account, and you shouldn't paste a personal access token into a chat. Both commits sit on top of your existing `Initial commit`, so nothing gets overwritten.

| Repo | Commit | Message |
|---|---|---|
| `Family_Appily_app` | `7a02be3` | Add build spec and design system extracted from physical wall charts |
| `Famiy_Appily_api` | `1afa004` | Add data contracts and surface the open backend architecture decision |

Pick one of the two paths below.

---

## Option 1 — Bundles (recommended)

Preserves the full commit messages. A git bundle is a single file that acts like a remote.

```sh
# App repo
git clone https://github.com/mspaldingworks/Family_Appily_app
cd Family_Appily_app
git pull /path/to/Family_Appily_app.bundle main
git push origin main
cd ..

# API repo
git clone https://github.com/mspaldingworks/Famiy_Appily_api
cd Famiy_Appily_api
git pull /path/to/Famiy_Appily_api.bundle main
git push origin main
```

Already have the repos cloned? Skip the `git clone` lines and run the rest inside your existing clones.

Verify before pulling if you like:

```sh
git bundle verify /path/to/Family_Appily_app.bundle
```

Both should report *"The bundle records a complete history."*

---

## Option 2 — Plain folders

If the bundles are inconvenient, copy the file trees in and commit yourself. You'll write your own commit messages.

```sh
cd /path/to/your/Family_Appily_app
cp -R /path/to/repos/Family_Appily_app/. .
git add -A
git commit -m "Add build spec and design system"
git push origin main
```

```sh
cd /path/to/your/Famiy_Appily_api
cp -R /path/to/repos/Famiy_Appily_api/. .
git add -A
git commit -m "Add data contracts and architecture decision"
git push origin main
```

The trailing `/.` on the source path matters — it copies the folder's *contents* including the `.gitignore`, rather than nesting the folder inside itself.

---

## What landed where

**`Family_Appily_app`**
```
CLAUDE.md                    ← build spec; Claude Code auto-loads this
README.md
.gitignore                   ← Xcode, SPM, and secrets
family-hub-assets/
  README.md
  data/         family.json, rotation.json, tickets.json
  design/       tokens.json, avatars/ (4 SVG), motifs/ (8 SVG)
  preview.html
```

**`Famiy_Appily_api`**
```
README.md
ARCHITECTURE_DECISION.md     ← read this before Phase 0
.gitignore                   ← env files, keys, service accounts
contracts/    family.json, rotation.json, tickets.json
```

---

## Two things to fix while you're in there

**The API repo name has a typo** — `Famiy_Appily_api`, missing the `l`. Rename it on GitHub now, before anything points at it. Settings → Repository name. GitHub redirects the old URL, then update your remote:

```sh
git remote set-url origin https://github.com/mspaldingworks/Family_Appily_api
```

**The three JSON contracts currently exist in both repos.** The app needs them locally to seed its store offline; the API repo holds them as the contract definition. Two copies of one schema will drift. Until the architecture decision in `ARCHITECTURE_DECISION.md` is settled, treat the app repo as the source of truth and mirror with:

```sh
cp ../Family_Appily_app/family-hub-assets/data/*.json contracts/
```
