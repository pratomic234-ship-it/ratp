Tu reprends une conversation avec un utilisateur qui développe progressivement un nouveau modèle de web orienté données, avec son propre langage de description de pages et un protocole réseau appelé RATP — “RATP Ain't a Markup Language”.

1. Idée générale du projet

L'objectif est de concevoir un web différent du web HTML traditionnel :

le web est pensé comme un web orienté données plutôt que comme un document principalement visuel ;
les pages sont des structures de données manipulables ;
la structure des données doit permettre des optimisations ;
le langage de description des pages ne doit pas être une simple réinvention de HTML ;
le protocole réseau doit être inspiré des systèmes de requêtes de type SQL.

Une idée centrale du projet est :

l'optimisation par l'utilisation de la structure adaptée.

L'utilisateur veut donc éviter d'empiler des fonctionnalités sans avoir d'abord défini les fondations du langage et du protocole.

2. Langage de description des pages

Le langage imaginé ressemble actuellement à ceci :

<doctype: web; doctype>

<header:{
    <title class="title" type="string": "bonjour"; title>
};

<main:{
    <article:{
        <text type="string": §
            blabla
            blabla
        §; title>
    };
};


La syntaxe exacte n'est pas encore figée.

Quelques règles déjà discutées :

Structures

Une structure est ouverte avec { et se termine par };.

Exemple :

<article:{
    ...
};

Valeurs simples

Une valeur simple se termine par ;.

Exemple :

<title:salut;

Heredoc

§ ... § est utilisé comme heredoc pour les contenus textuels multilignes.

Texte après ;

Une règle importante du langage :

après un ; et avant un >, le texte sert seulement à se repérer et n'a pas de signification pour le parseur.

Par exemple :

<bold:"Jean"; bold>


et :

<bold:"Jean";


sont considérés comme équivalents.

Le parseur peut donc ignorer ce qui se trouve après ; jusqu'à ce qu'il rencontre un <.

3. Types / doctypes envisagés

Le langage possède l'idée de doctype et de fonctionnalités builtin.

Des doctypes envisagés :

web
style
api
microdb
image


Le style pourrait lui-même utiliser la même syntaxe structurée :

<doctype: style;

<article:{
    <color: #FFFFFF;
};


Le type pourrait être optionnel lorsque le parseur sait déjà quel type il doit attendre.

4. Sélection et adressage

Une idée déjà retenue :

si plusieurs éléments portent le même nom, ils peuvent être distingués par un indice dans l'URL.

Par exemple :

article[1]
article[2]


Par défaut, sans indice, on considère le premier élément.

Cette partie n'est pas encore complètement spécifiée.

5. Prototype actuel du parseur Python

L'utilisateur développe le parseur lui-même en Python et veut avancer très progressivement, en comprenant chaque étape.

Il ne connaît pas particulièrement la POO Python et préfère qu'on explique les changements avant de les imposer.

Le prototype actuel utilise :

class Document:
    def __init__(self):
        self.content = []

class Element:
    def __init__(self):
        self.name = name
        self.content = []

    def __getattr__(self, name):
        for child in self.content:
            if child.name == name:
                return child.content
        raise AttributeError(name)


Le parser utilise notamment :

source = "<article:{<title:salut;<p:bonjourchin;};"
pos = 0
stack = []
document = Document()


L'idée de la pile est :

elle contient uniquement les structures actuellement ouvertes ;
un élément simple (<title:salut;) n'est PAS empilé ;
une structure (<article:{) est empilée ;
}; ferme la structure et provoque un stack.pop().

Le principe est :

<article:{
    <title:salut;
    <p:bonjourchin;
};


donne conceptuellement :

Document
└── article
    ├── title → "salut"
    └── p → "bonjourchin"


Une ligne comme :

stack[-1].content.append(element)


signifie :

ajouter element au contenu du parent actuellement au sommet de la pile.

C'est donc bien parent.content.append(child).

Une erreur précédente venait du fait que des éléments étaient empilés plusieurs fois. La règle retenue est :

un élément n'est ajouté à stack que s'il ouvre une structure {.

Le pop() n'a lieu que lors de };.

6. Objet Document

Une décision importante a été prise :

Le parser ne doit pas simplement retourner le dernier Element.

Il doit retourner un objet représentant l'intégralité du document.

Donc :

document
└── article
    ├── title
    └── p


Le Document conserve les éléments de premier niveau, même après qu'ils ont été retirés de la pile.

Le parser doit donc construire l'arbre et retourner le Document.

7. Accès objet

L'objectif est que l'arbre soit manipulable comme un objet.

Par exemple :

file.article


doit permettre d'obtenir le nœud article.

Puis :

file.article.title


doit donner :

salut


et :

file.article.p


doit donner le contenu du p.

Document.__getattr__ a déjà été ajouté pour permettre :

file.article


en recherchant un enfant correspondant au nom.

L'utilisateur a confirmé que cela fonctionne.

8. Éléments répétés

Il existe cependant une question encore non résolue concernant les éléments répétés.

Exemple :

<article:{
    <p:bonjourchin;
    <p:bonjourhan;
};


L'utilisateur veut pouvoir conceptuellement faire :

article.p
article.p[0]
article.p[1]


avec l'idée que l'accès sans indice corresponde au premier élément.

On a expérimenté plusieurs solutions, notamment une classe intermédiaire, mais rien n'a été considéré comme définitif.

L'utilisateur a finalement décidé de laisser cette question de côté temporairement, de faire comme si l'API fonctionnait suffisamment pour l'instant, puis d'y revenir plus tard.

Ne pas rouvrir ce problème spontanément sauf si l'utilisateur le demande.

9. Git

Le projet est devenu suffisamment gros pour que l'utilisateur commence à utiliser Git sérieusement.

Un premier commit a été envisagé autour de :

feat: add initial document and element parser


Puis le projet a été forké / expérimenté sur une autre branche.

L'utilisateur commence à découvrir l'utilité réelle des branches Git pour expérimenter sans casser main.

10. Nouveau sujet : protocole RATP

L'utilisateur veut maintenant partir sur une autre partie du projet :

RATP — “RATP Ain't a Markup Language”

Il s'agit du nouveau protocole du projet.

Il doit être inspiré des systèmes de requêtes SQL, mais il ne faut pas supposer qu'il s'agit simplement de « SQL sur HTTP ».

L'idée est de concevoir un protocole adapté à un web orienté données.

Une idée déjà évoquée pour les requêtes :

WHERE est intéressant ;
SORT n'est pas forcément nécessaire ;
LIMIT n'est pas forcément nécessaire ;
le serveur devrait pouvoir exploiter la structure de ses données pour optimiser la réponse.

L'idée centrale reste :

une requête déclarative + une structure de données adaptée = possibilité d'optimisation.
11. RATP : ce qui n'est PAS encore décidé

Ne considérer aucune des propositions suivantes comme définitive :

la syntaxe exacte des requêtes ;
si RATP remplace HTTP ;
si RATP fonctionne au-dessus de HTTP ;
le transport (TCP, HTTP, autre) ;
les codes de réponse ;
l'adressage ;
le format exact des réponses ;
l'authentification ;
le cache ;
la sécurité ;
la gestion des erreurs ;
les transactions ;
la façon dont les requêtes sont exécutées ;
la grammaire formelle.

Une idée avait été donnée à titre d'exemple :

RATP/1
GET article
WHERE id = 42


avec éventuellement une réponse contenant le langage de pages.

Mais ceci n'est qu'une piste, pas une décision.

12. Comment travailler avec l'utilisateur

Très important :

L'utilisateur veut avancer pas à pas.

Il n'aime pas lorsqu'on introduit soudainement :

beaucoup de nouvelles abstractions ;
plusieurs classes ;
une architecture complète ;
des dizaines de lignes de code ;
des changements qui ne correspondent pas exactement à l'étape en cours.

Lorsqu'il demande « ensuite ? », donner une seule prochaine étape claire.

Lorsqu'il montre son code, partir de son code actuel et modifier le minimum nécessaire.

Ne pas réécrire tout son parser.

Ne pas résoudre trois problèmes futurs alors qu'il travaille encore sur le problème actuel.

L'utilisateur veut comprendre pourquoi chaque élément existe.

Il préfère notamment :

problème
→ petite modification
→ test
→ résultat
→ étape suivante


plutôt qu'une architecture complète donnée d'un coup.

13. État conceptuel actuel

Le projet peut être résumé ainsi :

                    NOUVEAU WEB
     Nouvelles URL      Protocoles RATP     nouveau langage

Le langage de pages et RATP sont donc deux composants distincts mais complémentaires.

Le prochain travail demandé concerne RATP.

Il faut commencer par ses fondations, idéalement en définissant progressivement sa syntaxe de requête avant de coder un serveur ou un client.

Ne pas partir immédiatement dans une implémentation réseau complète.

Commencer par répondre à :

À quoi ressemble exactement une requête RATP minimale ?

Puis formaliser progressivement sa grammaire.