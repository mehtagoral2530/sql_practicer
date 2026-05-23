# Contributing

All changes follow **issue → branch → PR → merge**.

## Workflow

1. Open an issue (`bug`, `feature`, or `chore` template).
2. Create a branch from `main`: `cursor/short-description`.
3. Make changes and run tests when relevant:
   ```bash
   make up
   make test
   ```
4. Open a PR referencing the issue (`Closes #123`).
5. Merge to `main` after review and checks pass.

## Branch naming

- `cursor/fix-error-line-highlight`
- `cursor/add-lesson-window-functions`
- `cursor/update-readme-setup`

## Commit messages

One sentence focused on **why**, not just what.

## Do not

- Commit directly to `main` for feature work
- Force-push `main`
- Commit secrets (`.env`, tokens)
