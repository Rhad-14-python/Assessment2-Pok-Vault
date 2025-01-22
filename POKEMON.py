import requests
import tkinter as tk
from PIL import Image, ImageTk
import io

type_color_map = {
    'fire': '#F44336', 'water': '#2196F3', 'grass': '#4CAF50', 'electric': '#FFEB3B',
    'psychic': '#9C27B0', 'dark': '#424242', 'bug': '#8BC34A', 'normal': '#B0BEC5',
    'fairy': '#F48FB1', 'dragon': '#673AB7', 'steel': '#9E9E9E', 'fighting': '#D32F2F',
    'poison': '#8E24AA', 'ghost': '#7B62A3', 'rock': '#B8A038', 'ground': '#E0C068',
    'ice': '#98D8D8', 'flying': '#A890F0'
}

def fetch_pokemon_info(pokemon_name):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def display_pokemon_info():
    name_input = search_entry.get().strip().lower()
    pokemon_info = fetch_pokemon_info(name_input)

    if pokemon_info:
        name_label.config(text=pokemon_info['name'].capitalize())
        
        poke_type = pokemon_info['types'][0]['type']['name']
        bg_color = type_color_map.get(poke_type, '#FFD700')
        window.config(bg=bg_color)
        type_label.config(text=poke_type.capitalize(), bg=bg_color)

        sprite_url = pokemon_info['sprites']['front_default']
        sprite_data = requests.get(sprite_url).content
        sprite = Image.open(io.BytesIO(sprite_data)).resize((150, 150))
        sprite = ImageTk.PhotoImage(sprite)

        image_label.config(image=sprite)
        image_label.image = sprite

        stats_text = "\n".join([f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in pokemon_info['stats']])
        stats_label.config(text=stats_text)

        abilities = ", ".join([ability['ability']['name'].capitalize() for ability in pokemon_info['abilities']])
        abilities_label.config(text=f"Abilities: {abilities}")
    else:
        name_label.config(text="Invalid Pokémon!")
        image_label.config(image="", text="WHAT!?")
        stats_label.config(text="TYPE THE POKEMON'S NAME")
        abilities_label.config(text="CORRECTLY")

window = tk.Tk()
window.title("Pokédex App")
window.geometry("400x600")
window.config(bg="#FFD700")

search_entry = tk.Entry(window, font=("Arial", 14), bg="#D3D3D3", relief="solid", justify="center")
search_entry.place(x=50, y=20, width=300, height=30)

search_button = tk.Button(window, text="Search", font=("Arial", 14), command=display_pokemon_info, bg="#F4F4F9")
search_button.place(x=150, y=60, width=100, height=30)

name_label = tk.Label(window, text="Pokémon Name", font=("Arial", 12, "bold"), bg="white")
name_label.place(x=50, y=100, width=150, height=30)

type_label = tk.Label(window, text="Type", font=("Arial", 12, "bold"), bg="#FFD700")
type_label.place(x=210, y=100, width=140, height=30)

image_label = tk.Label(window, text="Image will appear here", font=("Arial", 20, "bold"), bg="#D3D3D3")
image_label.place(x=50, y=140, width=300, height=180)

stats_frame = tk.Frame(window, bg="white", bd=2, relief="ridge")
stats_frame.place(x=50, y=340, width=300, height=200)

stats_label = tk.Label(stats_frame, text="Stats will appear here", font=("Arial", 13, "bold"), bg="white", justify="left")
stats_label.pack(padx=10, pady=10, anchor="w")

abilities_label = tk.Label(stats_frame, text="Abilities will appear here", font=("Arial", 13, "bold"), bg="white")
abilities_label.pack(padx=10, pady=5, anchor="w")

window.mainloop()
