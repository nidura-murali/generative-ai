def build_success_response(merchant):
    return (
        f"Hey, here are the merchants you are looking for "
        f"Company Name: {merchant.get('merchantName')} "
        f"Address: {merchant.get('streetAddress')}, {merchant.get('city')} \n"
        f"State: {merchant.get('state')} - {merchant.get('postalCode')}\n"
        f"Country: {merchant.get('countryCode')}"
    )

def build_locationId_response(merchant):
    return(
        merchant.get('locationId')
    )

def build_not_found_response(id_type, id_value, country):
    return (
        f"No merchant found for {id_type} '{id_value}' in {country}. Please give it a try again"
    )