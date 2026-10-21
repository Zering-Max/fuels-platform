# Pipeline DBT du projet

## Qu'est ce que c'est ?

[DBT](https://docs.getdbt.com/) est un orchestrateur SQL, c'est à dire qu'il permet d'effectuer des requêtes SQL dans un ordre précis. Ces requêtes SQL peuvent dépendre des résultats des précédentes requêtes, ce qui permet in fine une longue transformation des données initiales, au fil des requêtes, pour obtenir des tables dans le format voulu et avec les croisements de données nécessaires.

## Comment utiliser les commandes DBT ?

_Se placer dans le dossier du projet dbt pour le faire tourner :_
```bash
cd data/dbt_pipeline
```

_Download dependencies :_
```bash
uv run dbt deps
```

_Lancer le dbt (run sans tests) :_
```bash
uv run dbt run
```

_Lancer le dbt complet avec tests :_
```bash
uv run dbt build
```

_Lancer uniquement mon model :_
```bash
uv run dbt run --select model mon_model.sql
```
_Lancer mon model et ses dépendances :_

**Upstream (models parents)**
```bash
uv run dbt run --select model +mon_model.sql
```
