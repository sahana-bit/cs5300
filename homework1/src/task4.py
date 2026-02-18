#Calculates discounted price
def calculate_discount(price, discount):
    if not isinstance(price, (int, float)):
        return "invalid data type for price"

    if not isinstance(discount, (int, float)):
        return "invalid data type for discount"

    final_price = price - (price*discount*0.01)
    return final_price