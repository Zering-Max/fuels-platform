import streamlit as st

st.markdown("## Méthodologie FAQ")
st.divider()

st.markdown("#### Quelles sources de données sont utlisées ?")

url = "https://www.data.gouv.fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-amelioree"
url_2 = "https://www.fiches-auto.fr/consommation/"
st.markdown("Pour les flux de données carburants, il s'agit de la source de DataGouv ([Lien](%s))." % url)
st.markdown("Pour les données de véhicules, la donnée a été récupérée par scrapping sur ce [site](%s)." % url_2)

st.markdown("#### Comment sont calculées les économies nettes ?")

st.markdown("Elles sont calculées en fonction des stations présentes dans un cercle calculé via les données d'adresse et de rayon d'action. Cela va calculer les économies à partir du prix maximum par litre des prix des stations présentes dans ce cercle.")

st.markdown("#### Est ce que le calculateur prend en compte les pénuries éventuelles des stations ?")

st.markdown("Tout à fait. Les données de flux de carburants sont mis à jour pour le moment toutes les 3 heures. Le calcul prend en compte le fait, sur cette fréquence de mise à jour, si une station est en pénurie. Elle ne sera alors pas proposée sur la carte quand bien même les économies nettes seraient avantageuses.")

st.markdown("#### Y'a-t-il vraiment toutes les stations en France ?")

st.markdown("Il y en a environ 10 000 recensées dans les données de DataGouv. Cependant, il a été remarqué que cela ne prend pas en compte les données des stations présentes dans les super/hypermarchés.")

