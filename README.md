## Electirck_Light_orchestra Project

## Prérequis
- Docker 20+
- Docker Compose 2.2

## Lancement
- cp .env.exemple .env # faire les modifications nécessaire
- make # se laisser guider par le help par default

## Aide par étape
- 1. make build pour build les containers qui en ont besoin
- 2. make up pour up tous les containers
- 3. make cli pour tester que tout fonctionne comme prévu
- 4. make monitoring pour voir si prometheus n'a pas échoué. Dois ouvrir deux pages dans le navigateur
  
## Accès interfaces
- 1. Orchestrateur: http://localhost:5042
- 2. Prometheus: http://localhost:9090
- 3. Grafana: http://localhost:3000 (admin/admin)

## Prochiane étape faire en sorte de récupérer du texte.
- 1. La page html fonctionne
- 2. Mais je n'aarive pas é récupérer le texte.
- 3. Peut être créeer un fichier avec l'extension .c