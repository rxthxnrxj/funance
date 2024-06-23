import pandas as pd
from .models import UserIntriguerInteraction

def prepare_interaction_data():
    interactions = UserIntriguerInteraction.objects.all().values('user', 'intriguer', 'liked')
    df = pd.DataFrame(interactions)
    return df