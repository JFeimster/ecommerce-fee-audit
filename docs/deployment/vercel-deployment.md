# Vercel Deployment

## Recommended Project Settings

- Repository: `JFeimster/ecommerce-fee-audit.vercel.app`
- Production Branch: `main`
- Root Directory: `site`
- Framework Preset: Other
- Build Command: leave empty
- Install Command: leave empty
- Output Directory: leave empty

## Deployment Lock

The repository-level `vercel.json` initially disables Git-triggered deployments for all branches, including `main`.

To permit a production deployment, change:

```json
"main": false
```

to:

```json
"main": true
```

After verification, return it to `false` when production deploys should be locked again.
