
Mode d'installation

1- Charger le dossier universal et le fichier Main.py (Streamlit)
2- installer le package de marigold avec la commande suivante Pip instal universal
3- installer les packages suivant:
	pip install pandas_datareader
	pip install yfinance
	pip install statsmodels
	Pip install seaborn
info pour installer streamlit il faut lancer la commande suivante: pip install streamlit. Dans notre cas nous avons utilisé Pychar comme editeur

Dans le repertoire universal on retrouve les algos de marigold ainsi que notre algo nommée reversaltrend.py
Pour le chargement des tickers, nous avons crée deux fonctions dans le fichier tools.py nommées: getData et GetTickersData 
pour lancer le Streamlit, utiliser la commande suivante: streamlit run Main.py