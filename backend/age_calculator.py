from backend.pyro_client import calculate_remote


def main() -> None:
    prompt = "Introduce tu fecha de nacimiento (DD/MM/AAAA o AAAA-MM-DD): "
    s = input(prompt)
    try:
        result = calculate_remote(s)
    except Exception as e:
        print(e)
        return
    print(f"Tienes {result['age']} años.")
    print(f"Tu signo zodiacal es {result['sign']}.")
    if result["days_until_next_birthday"] == 0:
        print("¡Feliz cumpleaños! Hoy es tu cumpleaños.")
    else:
        print(f"Faltan {result['days_until_next_birthday']} días para tu próximo cumpleaños.")


if __name__ == "__main__":
    main()