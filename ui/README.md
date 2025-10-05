# UI Project Setup Instructions

```shell
ng new agri-frame-survey-portal --routing --style=scss --prefix=af
cd agri-frame-survey-portal
ng generate module domains/survey --routing
npm i bootstrap

# Add Bootstrap CSS in angular.json:
# "node_modules/bootstrap/dist/css/bootstrap.min.css",

# Edit tsconfig.json → compilerOptions:

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