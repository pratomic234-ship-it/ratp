
# TODO

## Parseur et contenu inline

- [ ] Construire une chaîne d'affichage à partir de `inline_content` : conserver les chaînes et convertir les `Element` avec `str()`.
- [ ] Ajouter un test durable vérifiant l'ordre texte / élément inline / texte après l'élément.
- [ ] Décider précisément quand `§ ... §` représente un heredoc textuel et quand il contient du markup inline, puis documenter la règle. {cm:2026-11-20}

## Langage et doctypes

- [ ] Fixer les règles de grammaire encore ouvertes, sans confondre syntaxe du langage et comportement du parseur.
- [ ] Décider quelles significations et quels éléments builtin dépendent du doctype (par exemple `p` pour `web`, `line` pour un document vectoriel).
- [ ] Implémenter les dictionnaires par doctype qui sélectionnent les types et attributs builtin, puis les utiliser dans le code.
- [ ] Définir les attributs réservés : `defaultclass` et `id`. Le runtime attribue `id`; préciser quand et comment il gère `defaultclass`.
- [ ] Définir les attributs builtin modifiables : `type` et `class`, notamment les valeurs/types acceptés et leur effet.
- [ ] Définir le traitement des attributs libres, qui sont conservés sans comportement builtin.

## Adressage

- [ ] Reprendre plus tard l'accès aux éléments répétés et leur adressage par indice dans les URL. Sujet différé.

## Protocole RATP et sockets

- [ ] Définir la syntaxe et la sémantique des requêtes RATP ; `SELECT`, `FROM` et `WHERE` restent des pistes, pas une spécification.
- [ ] Décider du rôle de `WHERE`, `SORT` et `LIMIT`, et de la façon dont la structure des données peut optimiser les réponses.
- [ ] Définir séparément le transport TCP : échange d'octets, délimitation de fin de requête et format de réponse.
- [ ] Construire un échange client/serveur minimal par étapes, avec un test à chaque étape.