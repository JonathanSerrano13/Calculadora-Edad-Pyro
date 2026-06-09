import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.pyro_client import calculate_remote


def main() -> None:
    prompt = "Introduce tu fecha de nacimiento (DD/MM/AAAA o AAAA-MM-DD): "
    s = input(prompt)
    try:
        result = calculate_remote(s)
    except Exception as e:
        print(e)
        return
    print(f"Tienes {result['age']} años y naciste en {result['weekday']}.")
    print(f"Tu signo zodiacal es: {result['sign']}")
    print(f"Tu próximo cumpleaños será dentro de: {result['days_until_next_birthday']} días.")
    print("Llevas de vida:")
    print(f"En meses: {result['months_lived']}")
    print(f"En semanas: {result['weeks_lived']}")
    print(f"En días: {result['days_lived']}")


if __name__ == "__main__":
    main()