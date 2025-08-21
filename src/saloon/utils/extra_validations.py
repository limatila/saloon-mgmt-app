from datetime import datetime
from dateutil import relativedelta
from saloon.models import Client

def verify_client_is_active(client: Client) -> bool:
    return client.date_created >= (datetime.now() - relativedelta(years=3))

def verify_active_existant_client_with_phone_has_same_name(form_client_number: str, form_client_name: str) -> bool:
    if not form_client_number or form_client_name: raise Exception("Error in verifying existant clients by phone.")
    
    client_phone = Client.objects.filter(phone_number=form_client_number).first()
    if client_phone:
        if verify_client_is_active(client_phone):
            words = form_client_name.split()
            existant = False
            for word in words:
                if word in client_phone.name:
                    existant = True
                else: existant = False
                
            return existant #True if every name is found (not considering order)
    
    return False #not found client or name