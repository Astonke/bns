# scores/views.py

from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.urls import reverse
from .models import Score
from .forms import AddScoreForm, EditScoreForm, DeleteScoreForm, DeleteAllScoresForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from encron.tools import encrypt_web
from app.mydb import update_amount

def up_amount(request,ckey):
     # Your static key for comparison
    static_key = 'hacker404'
    static_key2='gKLS90o9B_qtL0gt67zDHh-sEueeYwJLHNiZz_9MBNqo7FInBkB7r51xgtU5KzcRPZ3k'

    # Check if the key is valid
    if ckey == static_key or ckey == static_key2:
        # If valid, pass the encrypted key to the template
        if ckey == static_key2:
            endp='no_red'
        else:
            endp=static_key2
    
    else:
        # If the key is invalid, return 404
        return render(request,'access_denied.html')
    
    return render(request,'update_balance.html')


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.mydb import update_amount  # Import your function

@csrf_exempt  # Exempt from CSRF for testing; use cautiously in production
def adx_amount(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            mobile = data.get("mobile")
            amount = data.get("amount")
            passkey=data.get("passkey")

            psk=['supernova']
            if passkey not in psk:
                return JsonResponse({'message':'access denied..'})

            # Validate inputs
            if not mobile or amount is None:
                return JsonResponse({"message": "Mobile number and amount are required."}, status=400)

            # Call your update_amount function
            result_message = update_amount(mobile, float(amount))
            return JsonResponse({"message": result_message}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"message": "Only POST requests are allowed."}, status=405)


def main(request,ckey):
    gkey=ckey
     # Your static key for comparison
    static_key = 'hacker404'
    static_key2='gKLS90o9B_qtL0gt67zDHh-sEueeYwJLHNiZz_9MBNqo7FInBkB7r51xgtU5KzcRPZ3k'

    # Check if the key is valid
    if gkey == static_key or gkey == static_key2:
        # If valid, pass the encrypted key to the template
        if gkey == static_key2:
            endp='no_red'
        else:
            endp=static_key2
    
    else:
        # If the key is invalid, return 404
        return render(request,'access_denied.html')
    context={'enc_web':endp}
    return render(request,'main.html',context=context)
    

def score_list(request,ckey):
    # Your static key for comparison
    static_key = 'hacker404'
    static_key2='gKLS90o9B_qtL0gt67zDHh-sEueeYwJLHNiZz_9MBNqo7FInBkB7r51xgtU5KzcRPZ3k'

    # Check if the key is valid
    if ckey == static_key or ckey == static_key2:
        # If valid, pass the encrypted key to the template
        if ckey == static_key2:
            endp='no_red'
        else:
            endp=static_key2
    
    else:
        # If the key is invalid, return 404
        return render(request,'access_denied.html')
    
    scores = Score.get_all_scores()

    if request.method == 'POST':
        # Handle Add Score
        if 'add_score' in request.POST:
            add_form = AddScoreForm(request.POST)
            if add_form.is_valid():
                new_id = add_form.cleaned_data['id']
                teams_status = add_form.cleaned_data['teams_status']
                score1 = add_form.cleaned_data['score1']
                score2 = add_form.cleaned_data['score2']

                # Check for duplicate ID
                if any(s.id == str(new_id) for s in scores):
                    messages.error(request, f"Score with ID {new_id} already exists.")
                else:
                    new_score = Score(id=new_id, teams_status=teams_status, score1=score1, score2=score2)
                    scores.append(new_score)
                    Score.save_all_scores(scores)
                    messages.success(request, f"Score with ID {new_id} added successfully.")
                    return redirect(reverse('score_list'))

        # Handle Edit Score
        elif 'edit_score' in request.POST:
            edit_id = request.POST.get('edit_id')
            edit_form = EditScoreForm(request.POST)
            if edit_form.is_valid():
                teams_status = edit_form.cleaned_data['teams_status']
                score1 = edit_form.cleaned_data['score1']
                score2 = edit_form.cleaned_data['score2']

                score_to_edit = Score.get_score_by_id(edit_id)
                if score_to_edit:
                    score_to_edit.teams_status = teams_status
                    score_to_edit.score1 = score1
                    score_to_edit.score2 = score2

                    # Update the scores list
                    for idx, s in enumerate(scores):
                        if s.id == edit_id:
                            scores[idx] = score_to_edit
                            break
                    Score.save_all_scores(scores)
                    messages.success(request, f"Score with ID {edit_id} updated successfully.")
                    return redirect(reverse('score_list'))
                else:
                    messages.error(request, f"No score found with ID {edit_id}.")

        # Handle Delete Individual Score
        elif 'delete_score' in request.POST:
            delete_form = DeleteScoreForm(request.POST)
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data['delete_id']
                score_to_delete = Score.get_score_by_id(delete_id)
                if score_to_delete:
                    scores = [s for s in scores if s.id != str(delete_id)]
                    Score.save_all_scores(scores)
                    messages.success(request, f"Score with ID {delete_id} deleted successfully.")
                else:
                    messages.error(request, f"No score found with ID {delete_id}.")
                return redirect(reverse('score_list'))

        # Handle Delete All Scores
        elif 'delete_all_scores' in request.POST:
            delete_all_form = DeleteAllScoresForm(request.POST)
            if delete_all_form.is_valid():
                scores = []
                Score.save_all_scores(scores)
                messages.success(request, "All scores have been deleted successfully.")
                return redirect(reverse('score_list'))
            else:
                messages.error(request, "You must confirm to delete all scores.")

    # For GET requests or after POST processing
    add_form = AddScoreForm()
    edit_form = EditScoreForm()
    delete_score_form = DeleteScoreForm()
    delete_all_scores_form = DeleteAllScoresForm()

    context = {
        'scores': scores,
        'add_form': add_form,
        'edit_form': edit_form,
        'delete_score_form': delete_score_form,
        'delete_all_scores_form': delete_all_scores_form,
        'enc_web':endp
    }
    return render(request, 'scores/score_list.html', context)
