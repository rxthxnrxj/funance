from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .recommendation import recommend_intriguer
from .data_preparation import prepare_interaction_data
from .model_training import train_model
from django.db.models import F

from base.models import *

from .serializers import *

import random
from datetime import datetime

# df = prepare_interaction_data()
# model, user_id_mapping, intriguer_id_mapping = train_model(df)


# def show_intriguer_to_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     intriguer = recommend_intriguer(
#         user, model, user_id_mapping, intriguer_id_mapping)
#     return Response({'intriguer': intriguer.text, 'theme': intriguer.theme})


@api_view(['POST'])
def user_intriguer_response(request):
    data = request.data
    user = User.objects.get(username=data['username'])
    intriguer = Intriguer.objects.get(id=data['intriguer_id'])
    response = data['response']

    # Update the user interaction
    interaction, created = UserIntriguerInteraction.objects.get_or_create(
        user=user,
        intriguer=intriguer,
        defaults={'responded': True, 'liked': response}
    )

    if not created:
        interaction.responded = True
        interaction.liked = response
        interaction.save()

    if response:
        user.current_streak += 1
        user.points += intriguer.chunk
    else:
        user.current_streak = 0

    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak

    user.last_interaction = datetime.now()
    user.last_intriguer_shown = intriguer.last_shown
    user.save()

    # Update intriguer's times shown
    intriguer.times_shown += 1
    intriguer.last_shown = datetime.now()
    intriguer.save()

    # Fetch the next random intriguer
    new_intriguer = random.choice(Intriguer.objects.all())

    user_serializer = UserSerializer(user)
    intriguer_serializer = IntriguerSerializer(new_intriguer)

    response_data = {
        'user': user_serializer.data,
        'intriguer': intriguer_serializer.data,
    }

    return Response(response_data)


@api_view(['POST'])
def user_details(request):
    data = request.data
    user = User.objects.get(username=data['username'])
    print(user)
    serializer = UserSerializer(user)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['POST'])
def lander_details(request):
    data = request.data
    user = User.objects.get(username=data['username'])
    intriguer = random.choice(Intriguer.objects.all())

    user_serializer = UserSerializer(user)
    intriguer_serializer = IntriguerSerializer(intriguer)

    response_data = {
        'user': user_serializer.data,
        'intriguer': intriguer_serializer.data,
    }
    print(response_data)

    return Response(response_data)


@api_view(['GET'])
def get_leaderboard(request):
    # Query to fetch users sorted by points descending
    leaderboard_users = User.objects.annotate(
        score=F('points')).order_by('-points')
    # Serialize queryset
    leaderboard_data = [{'username': user.username, 'points': user.points,
                         'longest_streak': user.longest_streak} for user in leaderboard_users]
    print(leaderboard_data)
    # Return serialized data as JSON response
    return Response(leaderboard_data)
