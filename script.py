import json

def calculate_total_price(net_price, tax, city_tax):
    """Calculate total price with tax included."""
    return float(net_price) + float(net_price) * (tax + city_tax)

# Reading from a JSON file
with open('Python-task.json', 'r', encoding="UTF-8") as file:
    data = json.load(file)

    # Find the cheapest (lowest) price
    shown_price_dict = data["assignment_results"][0]["shown_price"]
    currency = data["assignment_results"][0]['currency']

    lowest_price = float('inf')
    cheapest_room_type = ""

    for room_type, price in shown_price_dict.items():
        if float(price) < float(lowest_price):
            lowest_price = price
            cheapest_room_type = room_type

    print(f"Lowest shown price: {float(lowest_price):.2f} {currency}")

    # Number of guests assumption
    total_num_of_guest = data["assignment_results"][0]["number_of_guests"]
    total_num_of_rooms = len(shown_price_dict)
    guests_per_room = total_num_of_guest / total_num_of_rooms
    print(f"Room type: {cheapest_room_type}, number of guest with the cheapest price - {guests_per_room:.0f}")

    # Total price calculation with tax
    tax_value_str = data["assignment_results"][0]["ext_data"]['taxes'].strip("'")
    tax_value_dict = json.loads(tax_value_str)
    tax = float(tax_value_dict["TAX"]) / 100
    city_tax = float(tax_value_dict["City tax"]) / 100
    net_price = data["assignment_results"][0]["net_price"]

    room_type_w_total_price = []

    for room_type, price in net_price.items():
        total_price = calculate_total_price(price, tax, city_tax)
        room_type_w_total_price.append(f"Room type: {room_type}, total price: {total_price:.02f} {currency}")
        print(f"Room type: {room_type}, total price: {total_price:.02f} {currency}")

    # Prepare output data
    output_dict = {
        "output": [
            {"Lowest shown price": f"{lowest_price} {currency}"},
            {"Room type with number of guests": f"Room type: {cheapest_room_type}, number of guests: {guests_per_room:.0f}"},
            {"Room type with total price": room_type_w_total_price}
        ]
    }

    # Write output to a file
    with open('output.json', 'w', encoding="UTF-8") as output_file:
        json.dump(output_dict, output_file, indent=4)
