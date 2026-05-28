# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A static documentation repo: nine PlantUML diagram sources at the repo root that together describe the **S3-Platform** (seven separate Python/TypeScript/Helm repos under the `s3-platform-inc` org). There is no application code here — the only "build" is rendering `.puml` → PNG + SVG into `out/`.

Read `README.md` for the per-diagram index and the platform scope.

## Commands

```sh
# Syntax-check every diagram (what CI runs as its "test")
bash scripts/test.sh

# Render everything to out/ (matches CI)
plantuml -tpng -o "$(pwd)/out" *.puml
plantuml -tsvg -o "$(pwd)/out" *.puml

# Render one file while iterating
plantuml -tsvg 04a-sequence-n8n-trigger.puml

# Quick check on one file without producing output
plantuml -checkonly 05-component.puml
```

Local prereqs: `plantuml` and `graphviz` (`apt-get install plantuml graphviz` / `brew install plantuml graphviz`). The Smetana pragma (see below) lets diagrams render even when `graphviz` isn't installed.

## Architecture notes

**Diagram naming is load-bearing.** `NN[a-z]-<type>-<topic>.puml`. The leading number controls reading order; the type matches one of the six allowed kinds (`archimate3`, `use-case`, `activity`, `sequence`, `component`, `deploy`). Keep new diagrams in this pattern and add a row to the README table.

**The Smetana pragma** — diagrams whose layout PlantUML normally delegates to Graphviz (`archimate3`, `use-case`, `component`, `deploy`) start with:

```
@startuml
!pragma layout smetana
```

Activity and sequence diagrams use PlantUML's built-in layout and don't need it. If you add a new component/deploy/use-case/archimate diagram, include the pragma so it renders without `dot`.

**Identifier fidelity** — the diagrams quote real names from the seven platform repos (`PushTrigger`, `dbTask.relevant(node)`, `S3PParserBase`, `S3Plugin.download()`, `documents.add_document` DB function, `score_added` NOTIFY channel, `/auth/login`, `/tape`, `/score`, `/ws`, `s3-platform-credentials-{database,s3,github}`, `ghcr.io/s3-platform-inc/s3p-node:3.0.3-beta`, etc.). When editing, **don't paraphrase these** — they're the anchor to the actual code in `s3-platform-inc/{s3p-node, s3p-sdk, s3p-database, s3p-tape-service, s3p-web-annotation, s3p-n8n, cloud-core}`. If a name has drifted in the upstream repo, update it here too.

**ArchiMate syntax** — `01-archimate3-layered.puml` uses PlantUML's **native** `archimate #Layer "label" as alias <<stereotype>>` keyword. The macro-style library (`!include <archimate/Archimate>` with `Business_Actor(...)`, etc.) is **not bundled** with the PlantUML jar — don't switch to it. Available stereotypes are the kebab-case sprite names (e.g. `business-actor`, `application-component`, `technology-system-software`); they're listed via `unzip -l plantuml.jar | grep sprites/archimate/`.

## CI

`.github/workflows/render.yml` triggers on push to `main` (paths-ignore `out/**`, `README.md`, `.gitignore`), PRs touching `*.puml`/`scripts/test.sh`/`render.yml`, and manual dispatch. Steps: install plantuml+graphviz → `scripts/test.sh` → render PNG + SVG to `out/` → upload artifact → on push to main, commit refreshed `out/` back via `stefanzweifel/git-auto-commit-action` with message `ci: re-render diagrams [skip ci]`.

**Don't hand-commit `out/`.** CI owns it. Local renders into `out/` are fine for previewing — just don't push them in the same commit as a `.puml` change; CI will re-render anyway and you'd be reverting yourself on the next CI run. (`.gitignore` doesn't ignore `out/` so the first-commit baseline is browsable; CI updates supersede it.)

## Scope of edits

- New diagrams: add the `.puml`, run `scripts/test.sh`, add a row in `README.md`'s diagram table.
- Renaming a diagram changes the URLs of its rendered artifacts in `out/` — update the README and any external links.
- The six allowed diagram types are fixed (per the design brief); don't add `class`, `state`, `object`, `er`, etc. without confirming first.
