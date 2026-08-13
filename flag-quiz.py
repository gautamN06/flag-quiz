import flet as ft
import requests 
import os 
from dotenv import load_dotenv
import random

load_dotenv()

API_KEY = os.getenv("RESTCOUNTRIES_API_KEY")

response = requests.get(
    "https://api.restcountries.com/countries/v5?limit=100",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

data = response.json()

countries = data["data"]["objects"]
country = random.choice(countries)
correct_answer = country["names"]["common"]
flag_url = country["flag"]["url_png"]

wrong_answers = random.sample(
    [c["names"]["common"] for c in countries if c!= country],
    3
)

options = [correct_answer] + wrong_answers 
random.shuffle(options)

def main(page: ft.Page):
    page.title = "Flag Quiz"
    page.window.width = 500
    page.window.height = 600
    page.padding = 30

    def answer_click(e):
        selected_answer = e.control.content

        if selected_answer == correct_answer:
            print("Correct!")
        else:
            print("Incorrect!")

    flag_image = ft.Image(
        src=flag_url,
        width=300,
        height=200,
    )


    option_a = ft.Button(
        content=options[0],
        on_click=answer_click,
        width=300
    )

    option_b = ft.Button(
        content=options[1],
        on_click=answer_click,
        width=300
    )

    option_c = ft.Button(
        content=options[2],
        on_click=answer_click,
        width=300
    )

    option_d = ft.Button(
        content=options[3],
        on_click=answer_click,
        width=300
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Flag Quiz",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                flag_image,
                option_a,
                option_b,
                option_c,
                option_d
            ],
            spacing=15
        )
    )

ft.run(main)
