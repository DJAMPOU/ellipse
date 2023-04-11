import requests

def electric_vs_mechanic(stations):

    # Dictionnaire pour stocker le nombre de vélos mécaniques et électriques par ville
    velo_counts = {}

    # Parcourir chaque station et ajouter le nombre de vélos mécaniques et électriques par ville
    for station in stations:
        ville = station['contractName']
        velos = station['totalStands']['availabilities']['bikes']
        velos_mecanique = station['totalStands']['availabilities']['mechanicalBikes']
        velos_electrique = station['totalStands']['availabilities']['electricalBikes']

        if velos != velos_electrique + velos_mecanique or velos == 0:
            continue

        # Ajouter le nombre de vélos mécaniques et électriques à la ville correspondante
        if ville not in velo_counts:
            velo_counts[ville] = {
                'mecanique': 0,
                'electrique': 0,
                'total': 0
            }

        velo_counts[ville]['mecanique'] += velos_mecanique
        velo_counts[ville]['electrique'] += velos_electrique
        velo_counts[ville]['total'] += velos

    # Calculer le pourcentage de vélos mécaniques et électriques pour chaque ville
    for ville, count in velo_counts.items():
        total_velos = count['total']
        pourcentage_mecanique = count['mecanique'] / total_velos * 100
        pourcentage_electrique = count['electrique'] / total_velos * 100

        print(f"Ville: {ville}")
        print(f"Pourcentage de vélos mécaniques: {pourcentage_mecanique:.2f}%")
        print(f"Pourcentage de vélos électriques: {pourcentage_electrique:.2f}%")
        print("\n")

def bikes_by_city(contracts):

    # Initialisation du dictionnaire pour stocker le nombre de vélos par ville
    bikes_by_city = {}

    # Parcourir tous les contrats et compter le nombre de vélos pour chaque ville
    for contract in contracts:
        city_name = contract['name']
        url = f"https://api.jcdecaux.com/vls/v3/stations?contract={city_name}&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            stations = response.json()
            bike_count = sum([station['mainStands']['availabilities']['bikes'] for station in stations])
            bikes_by_city[city_name] = bike_count

    # Affichage du classement des villes avec le plus de vélos
    ranked_cities = sorted(bikes_by_city.items(), key=lambda x: x[1], reverse=True)
    print("Classement des villes avec le plus de vélos :")
    for i, (city, count) in enumerate(ranked_cities):
        print(f"{i + 1}. {city} : {count} vélos")


if __name__ == '__main__':
    # Clé API pour JCDecaux
    api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

    # URL de l'API JCDecaux pour récupérer les informations des stations de vélo
    url = f"https://api.jcdecaux.com/vls/v3/stations?apiKey={api_key}"
    # Récupérer les données de l'API
    response = requests.get(url)
    # Si la réponse est OK (code 200), extraire les informations des stations de vélo
    if response.status_code == 200:
        stations = response.json()

    # URL de l'API JCDecaux pour réccupérer les informations des contrats
    url = f"https://api.jcdecaux.com/vls/v3/contracts?apiKey={api_key}"
    # Récupération des données de l'API
    response = requests.get(url)
    # Vérification de la réponse de l'API
    if response.status_code != 200:
        print(f"Erreur lors de la récupération des données ({response.status_code})")
    # Conversion de la réponse en JSON
    contracts = response.json()

    electric_vs_mechanic(stations)
    bikes_by_city(contracts)