import requests
import tkinter as tk
from PIL import Image, ImageTk
import io

type_colors = {
    'fire': '#F44336', 'water': '#2196F3', 'grass': '#4CAF50', 'electric': '#FFEB3B',
    'psychic': '#9C27B0', 'dark': '#424242', 'bug': '#8BC34A', 'normal': '#B0BEC5',
    'fairy': '#F48FB1', 'dragon': '#673AB7', 'steel': '#9E9E9E', 'fighting': '#D32F2F',
    'poison': '#8E24AA', 'ghost': '#7B62A3', 'rock': '#B8A038', 'ground': '#E0C068',
    'ice': '#98D8D8', 'flying': '#A890F0'
}

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_pokemon():
    pokemon_name = search_entry.get().strip().lower()
    pokemon_data = get_pokemon_data(pokemon_name)

    if pokemon_data:

        pokemon_name_label.config(text=pokemon_data['name'].capitalize())

        pokemon_type = pokemon_data['types'][0]['type']['name']
        background_color = type_colors.get(pokemon_type, '#FFD700') 
        root.config(bg=background_color)
        type_label.config(text=pokemon_type.capitalize(), bg=background_color)

        image_url = pokemon_data['sprites']['front_default']
        image_data = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((150, 150))
        image = ImageTk.PhotoImage(image)

        image_label.config(image=image)
        image_label.image = image

        stats = pokemon_data['stats']
        stats_text = "\n".join([f"{s['stat']['name'].capitalize()}: {s['base_stat']}" for s in stats])
        stats_label.config(text=stats_text)

        abilities = ", ".join([a['ability']['name'].capitalize() for a in pokemon_data['abilities']])
        abilities_label.config(text=f"Abilities: {abilities}")

    else:
        pokemon_name_label.config(text="WHAT!?")
        image_label.config(image="", text="INVALID POKEMON")
        stats_label.config(text="TYPE THE POKEMON'S NAME")
        abilities_label.config(text="CORRECTLY")

root = tk.Tk()
root.title("PokéVault")
root.geometry("400x600")
root.config(bg="#FFD700")

search_entry = tk.Entry(root, font=("Arial", 14), bg="#D3D3D3", relief="solid", justify="center")
search_entry.place(x=50, y=20, width=300, height=30)

search_button = tk.Button(root, text="Search", font=("Arial", 14), command=search_pokemon, bg="#F4F4F9")
search_button.place(x=150, y=60, width=100, height=30)

pokemon_name_label = tk.Label(root, text="Pokemon name", font=("Arial", 12, "bold"), bg="white")
pokemon_name_label.place(x=50, y=100, width=150, height=30)

type_label = tk.Label(root, text="TYPE", font=("Arial", 12, "bold"), bg="#FFD700")
type_label.place(x=210, y=100, width=140, height=30)

image_label = tk.Label(root, text="^_____^", font=("Arial", 20, "bold"), bg="#D3D3D3")
image_label.place(x=50, y=140, width=300, height=180)

stats_frame = tk.Frame(root, bg="white", bd=2, relief="ridge",)
stats_frame.place(x=50, y=340, width=300, height=200)

stats_label = tk.Label(stats_frame, text="HP:\nDefense:\nAttack:\nSpeed:\nSpecial Attack:\nSpecial Defense:", font=("Arial", 13, "bold"), bg="white", justify="left")
stats_label.pack(padx=10, pady=10, anchor="w")

abilities_label = tk.Label(stats_frame, text="Abilities:", font=("Arial", 13,"bold"), bg="white")
abilities_label.pack(padx=10, pady=5, anchor="w")

root.mainloop()
