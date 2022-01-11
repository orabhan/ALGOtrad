import streamlit as st
import requests
import io
import datetime as dt
from universal.algos import *
from universal.algos.reversaltrend import ReversalTrend
from universal.tools import *

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.header("Les Inputs")
# sidebar pour les Moyennes mobile
Moyenne_Mobile_Long_Terme = st.sidebar.slider("Moyenne mobile long terme", 2, 50, 2)
Moyenne_Mobile_Court_Terme = st.sidebar.slider("Moyenne mobile court terme", 1, Moyenne_Mobile_Long_Terme, 1)

# DAte historique des données

Date_start = st.sidebar.date_input('Date de début', dt.date(2021, 1, 1))
Date_fin = st.sidebar.date_input('Date de Fin', dt.date(2021, 2, 1))
st.sidebar.subheader('Les Tickers')

#chargemenr de liste de tickers
url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(url).content
companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
Symbol_Tickers = list(companies["Company Name"].unique())

#Recup Libellés des tickers au lieu de mettre des nom de tickers
Nom_Tickers = st.sidebar.multiselect("", Symbol_Tickers)
index=companies[companies['Company Name'].isin(Nom_Tickers)].index
Sticker_Select=list(companies.loc[index,"Symbol"])


# Affichage du dataset
if len(Sticker_Select) > 1: #Sélectionner un minimun 2 tickers
    TickersData = tools.GetTickersData(Sticker_Select, Date_start, Date_fin)

    st.subheader("**Graphiques des actions**")
    st.write("Prix des actions technologiques")
    st.line_chart(TickersData)

    st.markdown(
        '''*Info: La rentabilité annuelle historique des actions sélèctionnées sont:*''')

    ret_stock = (np.log(TickersData / TickersData.shift()).mean()) * 252 * 100
    st.write(ret_stock)

    rt = ReversalTrend(Moyenne_Mobile_Court_Terme, Moyenne_Mobile_Long_Terme)
    # data = tools.data('nyse_o')
    result = rt.run(TickersData)
    st.write(pd.DataFrame(result.summary().split('\n'),index=None))

    result.plot(assets=False, logy=True, portfolio_label="ReversalTrend", bah=True, ucrp=True, bcrp=True, olmar=True, bnn=True, corn=True,crp=False,cwmr=False,eg=False,kelly=False,ons=False,pamr=False,rmr=False,up=False)
    st.pyplot()

    st.subheader("Résultat:")
    st.write("Pour le jour suivant, le model universalTrend vous propose les proportions d'investissement ci-dessous:")
    st.write(result.weights.tail(1))

    st.subheader("Histogramme des poids")
    result.plot_total_weights()
    st.pyplot()
else: st.write("Merci de séléctionner au moins deux actions svp")