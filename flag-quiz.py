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


def generate_question():
    country = random.choice(countries)

    correct_answer = country["names"]["common"]
    flag_url = country["flag"]["url_png"]

    wrong_answers = random.sample(
        [c["names"]["common"] for c in countries if c != country],
        3
    )

    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    return correct_answer, flag_url, options


def main(page: ft.Page):

    page.title = "Flag Quiz"
    page.window.width = 500
    page.window.height = 600
    page.padding = 30

    total_questions = 0
    current_question = 0
    score = 0

    title = ft.Text(
        "Flag Quiz",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    instructions = ft.Text(
        "How many questions would you like?"
    )

    question_text = ft.Text(size=18)

    result_text = ft.Text(
        size=18,
        weight=ft.FontWeight.BOLD
    )

    score_text = ft.Text(size=16)

    flag_image = ft.Image(
        src="https://flags.restcountries.com/v5/w640/us.png",
        width=300,
        height=200
    )

    option_a = ft.Button(width=300)
    option_b = ft.Button(width=300)
    option_c = ft.Button(width=300)
    option_d = ft.Button(width=300)

    def show_results():
        page.controls.clear()

        percentage = (score / total_questions) * 100

        page.add(
            ft.Column(
                controls=[
                    ft.Text(
                        "Quiz Complete!",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        f"Score: {score}/{total_questions}",
                        size=24
                    ),
                    ft.Text(
                        f"Accuracy: {percentage:.0f}%",
                        size=20
                    )
                ],
                spacing=20
            )
        )

        page.update()

    def show_question():
        nonlocal current_question

        current_question += 1

        correct_answer, flag_url, options = generate_question()

        option_a.data = correct_answer
        option_b.data = correct_answer
        option_c.data = correct_answer
        option_d.data = correct_answer

        option_a.content = options[0]
        option_b.content = options[1]
        option_c.content = options[2]
        option_d.content = options[3]

        flag_image.src = flag_url

        question_text.value = (
            f"Question {current_question}/{total_questions}"
        )

        score_text.value = f"Score: {score}"
        result_text.value = ""

        page.controls.clear()

        page.add(
            ft.Column(
                controls=[
                    title,
                    question_text,
                    flag_image,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    result_text,
                    score_text
                ],
                spacing=15
            )
        )

        page.update()

    def answer_click(e):
        nonlocal score

        selected_answer = e.control.content
        correct_answer = e.control.data

        if selected_answer == correct_answer:
            score += 1
            result_text.value = "Correct! ✓"
        else:
            result_text.value = (
                f"Incorrect! The correct answer is {correct_answer}."
            )

        score_text.value = (
            f"Score: {score}/{current_question}"
        )

        page.update()

        if current_question >= total_questions:
            show_results()
        else:
            show_question()

    option_a.on_click = answer_click
    option_b.on_click = answer_click
    option_c.on_click = answer_click
    option_d.on_click = answer_click

    def start_quiz(number_of_questions):
        nonlocal total_questions
        nonlocal current_question
        nonlocal score

        total_questions = number_of_questions
        current_question = 0
        score = 0

        show_question()

    five_button = ft.Button(
        content="5 Questions",
        on_click=lambda e: start_quiz(5),
        width=300
    )

    ten_button = ft.Button(
        content="10 Questions",
        on_click=lambda e: start_quiz(10),
        width=300
    )

    fifteen_button = ft.Button(
        content="15 Questions",
        on_click=lambda e: start_quiz(15),
        width=300
    )

    page.add(
        ft.Column(
            controls=[
                title,
                instructions,
                five_button,
                ten_button,
                fifteen_button
            ],
            spacing=15
        )
    )


ft.run(main)