# UI Project Setup Instructions

```shell
ng new agri-frame-survey-portal --routing --style=scss --prefix=af
cd agri-frame-survey-portal
ng generate module domains/survey --routing
npm i bootstrap
npm i @popperjs/core
npm i bootstrap-icons

# Add Bootstrap CSS in angular.json:
# "node_modules/bootstrap/dist/css/bootstrap.min.css",

# Edit tsconfig.json → compilerOptions:

# Core + Shared (cross-cutting + reusable UI)
mkdir -p src/app/core/{services,guards,interceptors}
ng g s app/core/services/config --flat
ng g g app/core/guards/auth --functional
ng g interceptor app/core/interceptors/auth-token --flat

# Shared (reusable components)
ng g module app/shared --flat
ng g c app/shared/components/header --standalone
ng g c app/shared/components/footer --standalone

# src/app/core/services/config.service.ts
# src/environments/environment.ts
# src/environments/environment.prod.ts

# Domains (backend models/services per bounded context)
# 4a) Survey domain
ng g module app/domains/survey --routing
ng g i app/domains/survey/models/survey --type=model
ng g i app/domains/survey/models/survey-summary --type=model
ng g s app/domains/survey/services/survey-api --flat

# src/app/domains/survey/models/survey.model.ts

# 4b) Analytics domain
ng g module app/domains/analytics --routing
ng g i app/domains/analytics/models/analytics-overview --type=model
ng g s app/domains/analytics/services/analytics-api --flat

# 4c) User/Admin domain (users, roles, tenants)
ng g module app/domains/user --routing
ng g i app/domains/user/models/user --type=model
ng g i app/domains/user/models/role --type=model
ng g s app/domains/user/services/user-api --flat

# 5) Features (UI flows, lazy routes per feature)
# 5a) Survey feature

ng g module app/features/survey --routing
ng g c app/features/survey/pages/survey-list --standalone
ng g c app/features/survey/pages/survey-viewer --standalone
ng g c app/features/survey/pages/survey-editor --standalone

# src/app/features/survey/survey-routing.module.ts

# 5b) Analytics feature
ng g module app/features/analytics --routing
ng g c app/features/analytics/pages/dashboard --standalone

# src/app/features/analytics/analytics-routing.module.ts

# 5c) Admin feature
ng g module app/features/admin --routing
ng g c app/features/admin/pages/users --standalone
ng g c app/features/admin/pages/roles --standalone
ng g c app/features/admin/pages/tenants --standalone

# src/app/features/admin/admin-routing.module.ts

# 6) Top-level routes (lazy-load all features)
# src/app/app.routes.ts

```


```shell
ng new agri-frame-survey-portal --routing --style=scss --prefix=af
cd agri-frame-survey-portal
npm i bootstrap
npm i ngx-favicon

# Scaffold features & pages
# Feature “modules” (flat, using standalone components)
mkdir -p src/app/{core,shared,features,domains}
mkdir -p src/app/domains/{survey,analytics,user}/{models,services,utils}
mkdir -p src/app/shared/components

# Domains: models + API service

ng g module core --flat
ng g s core/services/config --flat 

# Survey domain
ng g i app/domains/survey/models/survey --type=model
ng g i app/domains/survey/models/survey-summary --type=model
ng g s app/domains/survey/services/survey-api --flat

# (Stubs for other domains, optional now)
ng g i app/domains/analytics/models/analytics-overview --type=model
ng g s app/domains/analytics/services/analytics-api --flat
ng g i app/domains/user/models/user --type=model
ng g s app/domains/user/services/user-api --flat

# npm install @angular/flex-layout @angular/cdk
# npm install @ngx-translate/core @ngx-translate/http-loader
```