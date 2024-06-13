# Paint Application

Paint Application est une application de dessin simple développée en Python à l'aide de la bibliothèque Tkinter et Pillow pour la manipulation d'images.

## Fonctionnalités/Utilisation

- **Outils de dessin** : Utilisation d'un pinceau et d'un outil de remplissage pour dessiner sur un canevas.
- **Sélection de couleur** : Choix de la couleur de dessin à l'aide d'une palette de couleurs.
- **Sauvegarde et chargement d'images** : Fonctionnalités pour sauvegarder et charger des images au format JPG.
- **Nouvelle image** : Cliquez sur `File -> New` pour créer une nouvelle image avec des dimensions spécifiques.
- **Charger une image** : Utilisez `File -> Load` pour charger une image à partir de votre système de fichiers.
- **Sauvegarder une image** : Utilisez `File -> Save as` pour sauvegarder l'image actuelle sous un nouveau nom.
- **Outils de dessin** : Sélectionnez l'outil de dessin (`Quill` pour le pinceau, `Paint can` pour le remplissage) à partir de la barre d'outils.
- **Redimensionnement de l'image** : Faites glisser la poignée dans le coin inférieur droit pour redimensionner l'image.
- **Undo/Redo** : Utilisez `Edit -> Undo` et `Edit -> Redo` ou les raccourcis clavier `Ctrl+Z` et `Ctrl+Y` pour annuler et rétablir les actions de dessin.


## Présentation visuelle du projet

1. **Capture d'écran :**

    ![Capture d'écran de l'application Paint](Images/Screenshot.png)

2. **Vidéo de présentation :**

    ```bash
    insérer le lien vers la vidéo



## Prérequis

Pour exécuter l'application localement, vous aurez besoin des outils suivants installés sur votre machine :

- Python 3.x
- Tkinter
- Pillow (PIL)

## Installation et exécution

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/votre-utilisateur/paint-application.git
   cd paint-application

2. **Installez les dépendances**

    ```bash
    pip install -r requirements.txt

3. **Exécutez le fichier principal**

    ```bash
    python Shlag_Paint GUI.py

## Répartition des points

| Hugo | Sylvain | Marine | Trung | Khai |
|-----------|-----------|-----------|-----------|-----------|
| 20 %   | 25 %   | 15 %   | 20 %   | 20 %   |

## Explication des algorithmes non triviaux

1. **Outil remplissage :**

    L'outil de remplissage utilise une version spécialisée de l'algorithme "flood fill". Cet algorithme remplace une couleur spécifique sur le canevas par une autre couleur choisie par l'utilisateur. Lorsqu'on clique sur une zone du canevas avec l'outil de remplissage activé, l'algorithme détecte la couleur de la zone cliquée et remplace cette couleur, ainsi que toutes les zones adjacentes de la même couleur, par la nouvelle couleur sélectionnée. Ce processus se poursuit jusqu'à ce que toutes les zones connectées de la couleur d'origine soient remplies.

2. **Conversion en ASCII :**

    La conversion en ASCII permet de transformer des images en art ASCII, un processus qui consiste à représenter une image à l'aide de caractères ASCII au lieu de pixels. Pour ce faire, nous avons récupéré une liste de 93 caractères sur Internet, classée selon l’intensité lumineuse croissante de chaque caractère. Liste disponible sur : https://stackoverflow.com/questions/30097953/ascii-art-sorting-an-array-of-ascii-characters-by-brightness-levels-c-c

    La conversion des pixels en caractères ASCII est basée sur l'intensité lumineuse des pixels. Chaque pixel de l'image redimensionnée est parcouru, et son intensité moyenne est calculée - ici, il s’agit de la moyenne des 3 valeurs R, G, B. Cette intensité moyenne est ensuite comparée avec les caractères dans la liste de caractères ASCII, et le caractère ayant l’intensité lumineuse la plus proche de l’intensité moyenne est choisi pour représenter le pixel. Le caractère correspondant est ajouté à une chaîne de caractères représentant la ligne courante de l'image en ASCII. Cette chaîne de caractères est ensuite enregistrée dans un fichier texte créé.

    Pour afficher ce fichier texte dans un canevas, nous avons d’abord construit un nouveau type de canevas dit "zoomable". Cela a pour but de s'adapter à la taille de l'image, qui est grande en comparaison avec la taille de l’écran d’ordinateur. Sinon, l’utilisateur peut également choisir de réduire la taille de leur image avant de la convertir en art ASCII. L’affichage du texte sur le canevas se fait par une boucle qui lit chaque caractère de chaque ligne et colonne dans le fichier texte. Pour la clarté de l'image "ASCII", un espacement de 10 pixels entre les caractères est défini durant l'affichage.   

3. **Undo & Redo :**

    En général, les applications de dessin comme Paint utilisent le modèle de commande pour implémenter les fonctionnalités d’annulation  (Undo) et de rétablissement (Redo):

    - Chaque action que vous effectuez dans l’application (comme dessiner une ligne ou remplir une zone avec de la couleur) est encapsulée dans un objet de commande. Cet objet de commande contient toutes les informations nécessaires pour effectuer l’action (par exemple, le type de forme, les coordonnées de début et de fin, la couleur, etc.) et pour l’annuler et chaque fois que vous effectuez une action, l’objet de commande correspondant est ajouté à une pile de commandes.
    - Annuler (Undo) : Lorsque vous cliquez sur le bouton “Undo”, l’application retire la dernière commande de la pile et annule l’action correspondante. Cela est généralement réalisé en appelant une méthode undo() sur l’objet de commande, qui sait comment annuler l’action spécifique.
    - Rétablir (Redo) : Si vous avez annulé une action et que vous voulez la rétablir, l’application peut simplement réexécuter la commande correspondante. Cela est généralement réalisé en appelant une méthode redo() sur l’objet de commande.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez améliorer l'application Paint, veuillez ouvrir une issue pour discuter des changements proposés.