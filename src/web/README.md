# Contoso Trek Web

Vue 3 + Vuetify storefront for the Azure SRE Agent demo.

## Run locally

```powershell
cd src\web
npm install
npm run dev
```

The Vite dev server proxies `/api` and `/health` to `http://localhost:8080`.

## Build and test

```powershell
npm run build
npm test
```

## Runtime environment

The nginx container listens on port `8080`.

- `API_URL`: upstream API base URL for nginx proxying, for example `https://ca-trek-api-demo.<region>.azurecontainerapps.io` or `http://trek-api:8080` in Docker.

The web container also exposes `/healthz` for its own health probe.
