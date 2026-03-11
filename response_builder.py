def build_success_response(merchant):
    # return (
    #     f"Merchant Found :"
    #     f"Name: {merchant.get('merchantName')} "
    #     f"Address: {merchant.get('streetAddress')}, {merchant.get('city')} "
    #     f"State: {merchant.get('state')} - {merchant.get('postalCode')}"
    #     f"Country: {merchant.get('countryCode')}"
    # )
    return({
        "locationId":merchant.get('locationId')
    })

def build_not_found_response(id_type, id_value, country):
    return (
        f"No merchant found for {id_type} '{id_value}' in {country}."
    )