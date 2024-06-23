# recommendation.py

from django.utils import timezone
from .models import Intriguer, UserIntriguerInteraction
from .data_preparation import prepare_interaction_data
from .model_training import train_model

import numpy as np


# Neural collaborative filtering
def recommend_intriguer(user, model, user_id_mapping, intriguer_id_mapping):
    user_id = user.id
    user_index = user_id_mapping.get(user_id)

    if user_index is None:
        intriguer = Intriguer.objects.exclude(userintriguerinteraction__user=user).order_by('-times_shown').first()
    else:
        intriguers = Intriguer.objects.exclude(userintriguerinteraction__user=user)
        intriguer_ids = [intriguer.id for intriguer in intriguers]
        intriguer_indices = [intriguer_id_mapping.get(intriguer_id) for intriguer_id in intriguer_ids]

        predictions = model.predict([np.array([user_index] * len(intriguer_indices)), np.array(intriguer_indices)])
        recommended_fact_index = np.argmax(predictions)
        recommended_fact_id = intriguer_ids[recommended_fact_index]
        intriguer = Intriguer.objects.get(id=recommended_fact_id)

    # Log the interaction
    UserIntriguerInteraction.objects.create(user=user, intriguer=intriguer, shown_at=timezone.now())
    # Update fact metadata
    intriguer.times_shown += 1
    intriguer.last_shown = timezone.now()
    intriguer.save()

    return intriguer
