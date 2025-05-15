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
- 4. make monitoring pour voir si prometheus n'a pas échoué. Dois ouvrir trois pages dans le navigateur
  
## Accès interfaces
- 1. Orchestrateur/comiplateur: http://localhost:5042
- 2. Prometheus: http://localhost:9090
- 3. Grafana: http://localhost:3000 (admin/admin)

## Autre utilisation
- 1. Un fichier test.c se trouve à la racine du projet
- 2. ELO se trouve également sur un server AWS http://13.53.158.163:5042/

## Chose à faire

- 1. Dans le ReadMe expliquer la marche à suivre pour préparer un server AWS
- 2. containeur pour interpréter le python
- 3. Faire un CSS et rendre la page présentable
- 4. DataBase MongoDB pour gérer les tokens et les droits des users