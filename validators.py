from string import capwords


def get_string(prompt: str) -> str:
    while True:
        if answer := capwords(input(prompt)):
            return answer

        else:
            print("\nError: the answer cannot be blank.")


def get_answer_yes_no(prompt: str) -> bool:
    while True:
        if answer := input(prompt).strip().lower():
            if answer in ["y", "yes"]:
                return True

            elif answer in ["n", "no"]:
                return False

            else:
                print("\nError: Answer must be 'y | yes' or 'n | no'.")

        else:
            print("\nError: Answer cannot be blank")


def get_positive_int(prompt: str) -> int:
    while True:
        try:
            quantity = int(input(prompt))

            if quantity <= 0:
                print("\nError: The quantity must be greater than zero.")
                continue

        except ValueError:
            print(
                "\nError: The quantity must be entered using a positive integer numbers like '1' or '2'"
            )
            continue

        return quantity
