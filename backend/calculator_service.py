from __future__ import annotations

from datetime import date, datetime
from typing import Any

import Pyro5.api as pyro

SIGN_ELEMENTS = {
    "Aries": "fuego",
    "Leo": "fuego",
    "Sagitario": "fuego",
    "Tauro": "tierra",
    "Virgo": "tierra",
    "Capricornio": "tierra",
    "Géminis": "aire",
    "Libra": "aire",
    "Acuario": "aire",
    "Cáncer": "agua",
    "Escorpio": "agua",
    "Piscis": "agua",
}


def parse_date(s: str) -> date:
    s = s.strip()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise ValueError("Formato de fecha no reconocido. Usa DD/MM/AAAA o AAAA-MM-DD.")


def calculate_age(birthdate: date, today: date | None = None) -> int:
    if today is None:
        today = date.today()
    years = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        years -= 1
    return years


def days_until_next_birthday(birthdate: date, today: date | None = None) -> int:
    if today is None:
        today = date.today()
    try:
        next_bday = date(today.year, birthdate.month, birthdate.day)
    except ValueError:
        if birthdate.month == 2 and birthdate.day == 29:
            next_bday = date(today.year, 3, 1)
        else:
            raise
    if next_bday < today:
        try:
            next_bday = date(today.year + 1, birthdate.month, birthdate.day)
        except ValueError:
            if birthdate.month == 2 and birthdate.day == 29:
                next_bday = date(today.year + 1, 3, 1)
            else:
                raise
    return (next_bday - today).days


def zodiac_sign(birthdate: date) -> str:
    month = birthdate.month
    day = birthdate.day

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    if (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Tauro"
    if (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Géminis"
    if (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cáncer"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Escorpio"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagitario"
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricornio"
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Acuario"
    return "Piscis"


def sign_element(sign: str) -> str:
    return SIGN_ELEMENTS[sign]


def format_result(age: int, days: int, sign: str) -> str:
    birthday_text = (
        "¡Feliz cumpleaños!"
        if days == 0
        else f"Faltan {days} día(s) para tu próximo cumpleaños."
    )
    return f"Tienes {age} años. Tu signo zodiacal es {sign}. {birthday_text}"


@pyro.expose
class AgeCalculatorService:
    def calculate(self, birthdate_text: str, today_text: str | None = None) -> dict[str, Any]:
        birthdate = parse_date(birthdate_text)
        today = parse_date(today_text) if today_text else date.today()
        age = calculate_age(birthdate, today)
        days = days_until_next_birthday(birthdate, today)
        sign = zodiac_sign(birthdate)
        return {
            "birthdate": birthdate.strftime("%d/%m/%Y"),
            "today": today.strftime("%d/%m/%Y"),
            "age": age,
            "days_until_next_birthday": days,
            "sign": sign,
            "element": sign_element(sign),
            "message": format_result(age, days, sign),
        }

    def healthcheck(self) -> str:
        return "ok"