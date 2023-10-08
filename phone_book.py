records = {}


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Use help."
        except KeyError:
            return "Unknown record_id."
        except ValueError:
            return "Error: Invalid value format. Please enter valid data."

    return inner


@user_error
def greeting(*args) -> str:
    return "How can I help you?"


@user_error
def add_contact(*args):
    record_id = args[0]  # .lower()
    record_value = args[1]

    try:
        record_value = int(record_value)
    except ValueError:
        return "Error: Invalid value format. Please enter valid data."

    if record_id in records:
        return "Error: Contact with this ID already exists."
    records[record_id] = record_value
    return f"Contact: {record_id} with phone number: {record_value} added."


@user_error
def change_contact(*args):
    record_id = args[0]  # .lower()
    new_value = args[1]

    try:
        new_value = int(new_value)
    except ValueError:
        return "Error: Invalid value format. Please enter valid data."

    rec = records.get(record_id)
    if rec is not None:
        records[record_id] = new_value
        return f"Change contact: {record_id} with phone number: {new_value}"
    else:
        return "Error: Contact with this ID does not exist."


@user_error
def get_phone(*args):
    record_id = args[0]  # .lower()
    if record_id in records:
        return f"Phone number for contact '{record_id}' is {records[record_id]}."
    return f"Contact '{record_id}' not found."


@user_error
def show_all_contacts(*args):
    result = []
    max_id_length = max(len(record_id) for record_id in records.keys())

    for record_id, record_value in records.items():
        formatted_record_id = record_id.ljust(max_id_length)
        result.append(f"contact: {formatted_record_id} - phone: {record_value}")

    return "\n".join(result)


COMMANDS = {
    greeting: "hello",
    add_contact: "add",
    change_contact: "change",
    get_phone: "phone",
    show_all_contacts: "show all",
}

EXIT_COMMANDS = ("good bye", "close", "exit")


def parser(text: str):
    text_lower = text.lower()
    for func, kw in COMMANDS.items():
        if text_lower.startswith(kw):
            return func, text[len(kw) :].strip().split()
    return unknown, []


def unknown(*args):
    return "Unknown command. Try again."


def main():
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() in EXIT_COMMANDS:
            print("Good bye!")
            break

        func, data = parser(user_input)
        print(func(*data))


if __name__ == "__main__":
    main()
