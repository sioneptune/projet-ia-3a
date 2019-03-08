# Idées de base:

* Inividu pour jeu

* Créer jeu custom à concept simple (ex: roule loin/tue des bouboules)

* impt pouvoir crée le jeu nous-mêmes, pour plus de flexibilité

* Python? Python.

## Possibilités de jeu:

* Truc type Trial Extreme (moto terrain tourner+accelerer)

* Jeu avec bouboules/chars/trucs qui se tirent dessus, si tirent perdent "masse", si tue personne récupèrent une partie de leur "masse"

* Jeu de course/obstacle basique (i.e. Geometry dash)

* Impt: si jeu courses obstacles, pouvoir génerer terrain procéduralement, pour éviter le surapprentissage

Idée |Pour | Contre
:---: |:---: | :---:
Trial Xtreme | Sorties simples ( 2-4 outputs), individus simples | Inputs complexes, affichage chiant mais ça pas tres grave
Bouboules qui se tirent dessus | Affichage simplissime, input relativment simples => réseau rapide | Entrainement long surtout au début et potentiellement compliqué, peaufinage du code long
Geometry Dahslike | Terrain simple à coder, outputs ultra simples inputs très simples, terrain représentable par une bitmap | Génération procédurale à apprendre, surout si difficulté croissante

**Attention à la gestion du crossover si utilisons bibliothèques à la scikit-learn (ce qu'on va faire, hein, quand même (ou eventuellement numpy))**

## A garder en tête

* Threader les individus

* Pas nos propres réseaux de neurones, prendre library bien opti sa mère

* Garder la représentations des individus assez simples pour que le crossover ne soit pas un enfer

## Conclusion: on part sur les bouboules

* Le terrain ne sera pas plus dur à coder que l'algo lui-même

* Situations en constant changement => algo qui apprends à réagir (mieux?)

* Attention à bien gérer le début (faire jouer contre ~~I~~As super basiques, eg pattern prédéfini, ou "je vois je tire", ce genre de choses

* Deux phases: apprentissage contre IAs, apprentissage contre soi-même

* Mais bon, c'est une IA, donc ça sera quand même contre une IA, mais genre une meilleure IA tu vois

* Jeu contre soi-même: apprentissage quasi par tournois (simplifie VACHEMENT l'heuristique)

* Litteral survival of the fittest

* **Bien definir les règles du jeu**: Durer le plus longtemps? Buter le plus de bouboules? Être le plus *thicc*?

