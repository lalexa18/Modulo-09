import requests

BASE_URL = "https://swapi.dev/api/"

def get_all_data(endpoint):
    """Recupera todos los datos de un endpoint paginado."""
    url = f"{BASE_URL}{endpoint}/"
    data = []
    while url:
        response = requests.get(url).json()
        data.extend(response['results'])
        url = response.get('next')  # Obtiene la URL de la siguiente página, si existe.
    return data

def question_a():
    """¿En cuántas películas aparecen planetas cuyo clima sea árido?"""
    planets = get_all_data("planets")
    films_with_arid_climate = set()
    for planet in planets:
        if "arid" in planet["climate"]:
            films_with_arid_climate.update(planet["films"])
    return len(films_with_arid_climate)

def question_b():
    """¿Cuántos Wookies aparecen en toda la saga?"""
    species = get_all_data("species")
    wookie_species = next((s for s in species if s["name"] == "Wookiee"), None)
    if not wookie_species:
        return 0
    people = get_all_data("people")
    wookies = [person for person in people if person["species"] and wookie_species["url"] in person["species"]]
    return len(wookies)

def question_c():
    """¿Cuál es el nombre de la aeronave más pequeña en la primera película?"""
    films = get_all_data("films")
    first_film = next((film for film in films if film["episode_id"] == 4), None)
    if not first_film:
        return "No se encontró la primera película."
    starships = [requests.get(url).json() for url in first_film["starships"]]
    smallest_starship = min(starships, key=lambda s: float(s["length"]) if s["length"].replace('.', '', 1).isdigit() else float('inf'))
    return smallest_starship["name"]

if __name__ == "__main__":
    print(f"a) Número de películas con planetas de clima árido: {question_a()}")
    print(f"b) Número de Wookies en la saga: {question_b()}")
    print(f"c) Aeronave más pequeña en la primera película: {question_c()}")