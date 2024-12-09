from django.shortcuts import render
from app.my_func import *
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password  # For password hashing
from django.shortcuts import render, redirect  # For rendering templates and redirects
#from .models import User  # Import your User model from models.py
from django.contrib.auth import authenticate 
from app.mydb import *
from app.encrypted import *
import json
from encron.tools import *
from app.mpesa import mpesa_pr
from mysite.settings import CSRF_TRUSTED_ORIGINS
# views.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.utils.crypto import get_random_string

from django.utils.timezone import now

def referral_page(request, referral_code):
    try:
        referrer = User.objects.get(referral_code=referral_code)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid referral link"}, status=404)

    # Simulate a unique user (in real-world, track using user accounts or session)
    user_ip = get_client_ip(request)
    if not referrer.referrals.filter(mobile=user_ip).exists():  # Log unique visits based on IP or other identifiers
        referrer.referral_count += 1
        referrer.save()

    return render(request, 'referral_page.html', {'referrer': referrer})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from .referal import *

def generate_referral_code(mobile):
    return f"{mobile[:5]}-{get_random_string(5)}"

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
from django.urls import reverse
"""

"""
from django.urls import reverse
import logging

# Set up logging for error tracking
#logger = logging.getLogger(__name__)


def view_referrals(request):
    csv_file_path = find_file('referrals.csv')
    
    # Read the CSV file
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        referrals_data = []
        for row in reader:
            referrals_data.append({
                'mobile_number': row['mobile_number'],
                'referral_count': int(row['referral_count'])
            })

    # Pass the data to the template
    return render(request, 'view_referrals.html', {'referrals_data': referrals_data})

"""

"""
def generate_referral(request):
    if request.method == "POST":
        try:
            # Get the mobile number from the JSON request body
            body = json.loads(request.body)
            mobile = body.get('mobile', '').strip()

            # Ensure mobile number is provided
            if not mobile:
                return JsonResponse({"error": "Mobile number is required"}, status=400)

            # Generate or fetch referral code (you can still generate it or fetch from CSV if needed)
            referral_code = generate_referral_code(mobile)
            
            # Update the referral count in the CSV file
            referral_count = update_referral_count(mobile)
            
            # Generate referral link
            referral_link = request.build_absolute_uri(
                reverse('referral_page', kwargs={'referral_code': referral_code})
            )

            return JsonResponse({
                "referral_link": referral_link,
                "analytics": {
                    "referral_count": referral_count
                }
            })

        except Exception as e:
            logger.error(f"Error in generating referral: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return render(request, 'generate_referral.html')

#from django.shortcuts import render, redirect
from django.http import HttpResponse

# File paths (adjust based on your project structure)
BETSLIPS_FILE = find_file('pending_slips.csv')

# Helper to load data
def load_betslips(file_path=find_file("pending_slips.csv")):
    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        return list(reader)

def save_betslips(bets, file_path=find_file("pending_slips.csv")):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(bets)



from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect

def manage_bets_secure(request, key):
    static_key2 = "hacker404"  # Replace with your desired static key

    # Check if the key matches
    if key != static_key2:
        return render(request, 'access_denied.html')

    bets = load_betslips()  # Load all bets from the CSV file.

    # Filtered views
    pending_bets = [bet for bet in bets if bet[-1].strip().lower() == "pending"]
    won_bets = [bet for bet in bets if bet[-1].strip().lower() == "win"]
    lost_bets = [bet for bet in bets if bet[-1].strip().lower() == "fail"]

    # Handle modification
    print(f'request:{request}')
    if "modify_row" in str(request):
                row_index = int(request.GET.get("row_index"))
                new_status = request.GET.get("status").strip().lower()

                print(f'row:{row_index},status:{new_status}')

                # Validate status input
                if new_status not in ["pending", "win", "fail"]:
                    print('new_status error')
                    raise ValueError("Invalid status value. Allowed values: 'pending', 'win', 'fail'.")

                # Update the status in the list
                bets[row_index][-1] = new_status  # Update the last column in the row
                save_betslips(bets)  # Save changes to the CSV file.
                print('changes made')
                return redirect('manage_bets_secure', key=key)


    try:
        if request.method == "POST":
            print('post method used')
            print(request.POST)
            # Handle deletion
            if "delete_row" in request.POST:
                row_index = int(request.POST.get("row_index"))
                del bets[row_index]
                save_betslips(bets)  # Save changes to the CSV file.
                return redirect('manage_bets_secure', key=key)

            # Handle modification
            if "modify_row" in request.POST:
                row_index = int(request.POST.get("row_index"))
                new_status = request.POST.get("status").strip().lower()

                print(f'row:{row_index},status:{new_status}')

                # Validate status input
                if new_status not in ["pending", "win", "fail"]:
                    print('new_status error')
                    raise ValueError("Invalid status value. Allowed values: 'pending', 'win', 'fail'.")

                # Update the status in the list
                bets[row_index][-1] = new_status  # Update the last column in the row
                save_betslips(bets)  # Save changes to the CSV file.
                print('changes made')
                return redirect('manage_bets_secure', key=key)

    except (IndexError, ValueError) as e:
        print('possible index error')
        # Handle errors gracefully and pass them to the template for feedback.
        return render(request, 'manage_betslips.html', {
            'pending_bets': pending_bets,
            'won_bets': won_bets,
            'lost_bets': lost_bets,
            'error': str(e),
        })

    # Render the page with bet data and no errors.
    return render(request, 'manage_betslips.html', {
        'pending_bets': pending_bets,
        'won_bets': won_bets,
        'lost_bets': lost_bets,
        'error': None,
    })



# View for displaying and managing bets
def manage_betslips(request,ckey):
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
    
    bets = load_betslips()  # Load all bets from the CSV file.

    # Filtered views
    pending_bets = [bet for bet in bets if bet[-1].strip().lower() == "pending"]
    won_bets = [bet for bet in bets if bet[-1].strip().lower() == "win"]
    lost_bets = [bet for bet in bets if bet[-1].strip().lower() == "fail"]

    try:
        # Handle deletion
        if request.method == "POST" and "delete_row" in request.POST:
            row_index = int(request.POST.get("row_index"))
            del bets[row_index]
            save_betslips(bets)  # Save changes to the CSV file.
            return redirect('manage_betslips')

        # Handle modification
        if request.method == "POST" and "modify_row" in request.POST:
            row_index = int(request.POST.get("row_index"))
            new_status = request.POST.get("status").strip().lower()

            # Validate status input
            if new_status not in ["pending", "win", "fail"]:
                raise ValueError("Invalid status value. Allowed values: 'pending', 'win', 'fail'.")

            # Update the status in the list
            bets[row_index][-1] = new_status
            save_betslips(bets)  # Save changes to the CSV file.
            return redirect('manage_betslips')

    except (IndexError, ValueError) as e:
        # Handle errors gracefully and pass them to the template for feedback.
        return render(request, 'manage_betslips.html', {
            'bets': bets,
            'pending_bets': pending_bets,
            'won_bets': won_bets,
            'lost_bets': lost_bets,
            'error': str(e),
        })

    # Render the page with bet data and no errors.
    return render(request, 'manage_betslips.html', {
        'bets': bets,
        'pending_bets': pending_bets,
        'won_bets': won_bets,
        'lost_bets': lost_bets,
        'error': None,
    })


def manage_wins(request,ckey):
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

    wins_path = find_file('wins.csv')
    paid_path = find_file('paid.csv')
    
    # Load data from files
    wins_data = []
    paid_data = set()  # For faster lookups

    # Read paid.csv
    try:
        with open(paid_path, mode='r') as paid_file:
            reader = csv.reader(paid_file)
            for row in reader:
                paid_data.add(tuple(row))
    except FileNotFoundError:
        pass  # If paid.csv doesn't exist, continue

    # Read wins.csv, skipping paid rows
    try:
        with open(wins_path, mode='r') as wins_file:
            reader = csv.reader(wins_file)
            for row in reader:
                if tuple(row) not in paid_data:
                    wins_data.append(row)
    except FileNotFoundError:
        pass  # Handle no wins.csv file

    # Handle button click
    if request.method == "POST":
        row_data = request.POST.get("row_data")
        if row_data:
            # Append the row to paid.csv
            with open(paid_path, mode='a', newline='') as paid_file:
                writer = csv.writer(paid_file)
                writer.writerow(row_data.split(","))
            return redirect('manage_wins')  # Refresh the page

    return render(request, 'manage_wins.html', {'wins_data': wins_data})


#base_url=CSRF_TRUSTED_ORIGINS[0]
from .conf_base_url import base_url
#base_url='https://drum-clear-hawk.ngrok-free.app/'

def malic(request):
    return render(request,'malic.html')

@csrf_exempt
def check_ip(request,ckey):
    if request.method == 'POST':
        try:
            dec_data=decrypt_web('krypton',ckey)
            #print(dec_data)
            mobile, bal = dec_data.split(',')
            data = json.loads(request.body)
            ip_address = data.get('ip_address')

            print(f'user:{mobile},ip:{ip_address}')
            if check_if_blocked(mobile):
                return JsonResponse({'status':'redirect','redirect_url':'malic/'})

            # Here, you'd add your logic to check if the IP and mobile match
            if check_mobile_ip_match(mobile,ip_address):  # Custom logic for IP and mobile check
                return JsonResponse({'status': 'ok'})  # IP and mobile match, continue
            else:
                return JsonResponse({
                    'status': 'redirect',  # IP and mobile do not match
                    'redirect_url': 'login_page/'  # Redirect to the login page or another page
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_ip(request):
     ip_adr=request.META.get('REMOTE_ADDR')
     return ip_adr


def def_page(request):
    # Assuming this is your login URL
    #takeout old
    remove_past_matches(find_file('today.csv'))
    #reverse_csv_rows()
    html_page=generate_match_data_from_csv(find_file('clean.csv'))
    context = {'show_button': True,'show_depo': False,'def_js':True,'html_page':html_page}
    return render(request, 'home_def.html', context)


def login_page(request):
    context = {}  # You can add data to the context dictionary if needed
    return render(request, 'login.html', context)

def register_page(request):
    context = {} # You can add data to the context dictionary if needed
    return render(request, 'register.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # for demonstration only (remove in production)
#client_file('clients.csv')

def register(request):
    ip_address = get_ip(request)
    print(request.GET)
    print('\n')
    if request.method == 'GET':
        # Access data from request body
        name=request.GET.get('name')
        email=request.GET.get('email')
        psk=request.GET.get('password')
        mobile=request.GET.get('mobile')
        ip_address = request.GET.get('ip_address')
        print(name,email,psk,mobile)
        j_response = {'mobile': mobile, 'info': 'verified'}
        if auth_user(mobile, psk):
            j_response = {'redirect': True, 'info': 'user already exists'}
            #return JsonResponse(j_response)
            return render(request, 'login.html', j_response)
        else:
            balance='0'
            check_add(client_file,[name,email,str(psk),str(mobile),balance])
            add_mobile_ip_to_csv(mobile,ip_address)
            j_response = {'redirect': True, 'info': 'Account_created'}
            return render(request, 'login.html', j_response)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def login(request):
     # Get the IP address from the request META information
    #ip_address = get_ip(request)
    if request.method == 'POST':
        try:
            # Decode the request body to a string
            data = request.body.decode('utf-8')
            print("Received data:", data)
            
            # Parse the JSON string to a dictionary
            data = json.loads(data)
            
            # Access mobile number and password
            mobile_no = data.get('mobile')
            password = data.get('psk')
            ip_address=data.get('ip_address')

            if mobile_no is None or password is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            print("Mobile:", mobile_no, "Password:", password)
            
            # Authenticate user (this is a placeholder function, replace with actual logic)
            if auth_user((mobile_no), (password)):
                balance = get_balance(mobile_no)
                enc_data = f'{mobile_no},{balance}'
                web_key = encrypt_web('krypton', enc_data)
                print(web_key)
                j_response = {'redirect': True, 'info': 'verified', 'ckey': web_key}
                update_mobile_ip_in_csv(mobile_no,ip_address)
                return JsonResponse(j_response)
            else:
                j_response = {'redirect': True, 'info': 'invalid'}
                return JsonResponse(j_response)
            
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

    elif request.method == 'GET':
        return render(request, 'login.html')
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
  

def home_page(request, ckey):
    dec_data=decrypt_web('krypton',ckey)
    #print(dec_data)
    id, bal = dec_data.split(',')
    balance=get_balance(id)
    #takeout old
    remove_past_matches(find_file('today.csv'))
    #reverse to start with popular
    #reverse_csv_rows()
    html_page=generate_match_data_from_csv(find_file('clean.csv'))
    #print(base_url)
    context = {'show_button': False,'mobile': id ,'balanc':balance,'show_depo': True ,'def_js':False,'html_page':html_page,'page_base':base_url}
    return render(request,'home_def.html',context=context)


# Updated process_slip function with the check
def process_slip(request):
    if request.method == 'POST':
        try:
            # Decode the request body to a string
            data = request.body.decode('utf-8')
            # Parse the JSON string to a dictionary
            datas = json.loads(data)
            
            # Access picks and other details
            picks_str = datas['picks']
            mobile = datas['mobile']
            possible_win = datas['possible']
            odds = datas['odds']
            bet_amount = datas['bet_amount']
            max_time = datas['max_time']
            balance = get_balance(mobile)
            bt_amount = float(bet_amount)
            bal = float(balance)

            if bt_amount > bal:
                print(bt_amount, '>', bal)
                return JsonResponse({'info': 'deny'})
            if bt_amount <= bal:
                new_balance = bal - bt_amount
                update_balance(mobile, new_balance, bt_amount)

                # Parse the picks string to a dictionary
                picks = json.loads(picks_str)

                # Load original CSV data to validate picks
               # csv_data = load_csv_data(find_file('today.csv'))  # Provide the correct path to the CSV file
               # is_valid, validation_message = validate_picks(picks, csv_data)
                 
               # if not is_valid:
                   # return JsonResponse({'info': 'invalid', 'message': validation_message})

                # Set default status for each pick to 'pending'
                for key in picks:
                    picks[key]['status'] = 'pending'

                # The payload should be counter checked in the database for authenticity
                pending = find_file('pending_slips.csv')
                nw = [mobile, possible_win, json.dumps(picks), odds, max_time, 'pending']
                #print(f'new: {nw}')
                #print('arguments ok..')

                # Add to the database
                add_to_db(pending, nw)
                #print('added to db')
                return JsonResponse({'info': 'rec'})

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'info': 'error', 'message': str(e)})

import os

def pending(request, ckey):
    # Path to the pending_slips.csv file
    file_path = find_file('pending_slips.csv')
    
    # Check if the file is empty or doesn't exist
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        # If the file is empty or doesn't exist, render the template without context
        return render(request, 'pending2.html')
    
    # Decrypt data
    dec_data = decrypt_web('krypton', ckey)
    mobile, balance = dec_data.split(',')

    # Update pending slips and remove if started
    update_pending_slips()
    remove_if_started()

    # Retrieve client slips
    slips = get_client_slips(mobile)

    # Context for rendering
    context = {
        'mobile': mobile,
        'balanc': balance,
        'slips': slips
    }

    # Render template with context
    return render(request, 'pending2.html', context)

def mpesa_deposit(request,amount,ckey):
    if request.method == 'GET':
        try:
            dec_data = decrypt_web('krypton', ckey)
            mobile, bal = dec_data.split(',')
            n_char=['0','1','2','3','4','5','6','7','8','9']
            check_2_block_user(mobile,amount,n_char,JsonResponse,'rej_depo')
            depo=int(amount)
            if depo < 10:
                return JsonResponse({'info':'rej_depo'})
            else:
                try:
                    mpesa_pr(mobile,depo)
                    print('ussd sent..')
                    #return JsonResponse({'info':'wait_depo'})
                    id, bal = dec_data.split(',')
                    balance=get_balance(id)
                    html_page=generate_match_data_from_csv(find_file('today.csv'))
                    context = {'show_button': False,'mobile': id ,'balanc':balance,'show_depo': True ,'def_js':False,'html_page':html_page}
                    return render(request, 'home_def.html', context)
                except:
                    print('mpesa func error')
                    return JsonResponse({'error': 'Invalid JSON data'}, status=400)
                    
        except:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
    elif request.method == 'POST':
        return JsonResponse({'info': 'reload'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
from django.http import JsonResponse
import json


from django.http import JsonResponse
from .models import Withdrawal
import json


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

@csrf_exempt
def mpesa_withdraw(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            datas = json.loads(data)
            withdraw = datas['withdraw_amount']
            mobile = datas['mobile']

            balance = get_balance(mobile)
            #print(balance)
            #print(withdraw)
            if float(balance) < float(withdraw):
                return JsonResponse({'info': 'insufficient'})
            else:
                new_balance = float(balance) - float(withdraw)
                update_balance(mobile,new_balance,float(withdraw))
                # Save the successful withdrawal request
                Withdrawal.objects.create(
                    mobile=mobile,
                    amount=float(withdraw),
                    status='success',
                    timestamp=(time.strftime('%H:%M-%D'))
                )
                send_mail(
                          'initiate withdrawal',
                          f'Amount:{withdraw} \n mobile: {mobile}',
                          'crashcoders6@gmail.com',  # Replace with your email
                          ['crashcoders6@gmail.com'],  # Replace with your email
                          fail_silently=False,
                          )
                print('withdraw success')
                return JsonResponse({'info': 'wait_withdraw'})
        
        except:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
    elif request.method == 'GET':
        return JsonResponse({'info': 'reload'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def finance_page(request,ckey):
    dec_data = decrypt_web('krypton', ckey)
    mobile, balance = dec_data.split(',')
    bal=get_balance(mobile)
    #print(f'client_balance:{bal}')
    context = {
        'mobile': mobile,
        'balc': bal
    }
    return render(request, 'finance.html', context)

win_db=find_file('wins.csv')
loss_db=find_file('losses.csv')


def fail_slip(request):
    # Get the client ID and win amount from the URL
    client_id = request.GET.get('mobile')
    loss_amount = request.GET.get('win_amount')

    if client_id and loss_amount:
        try:
            check_add(loss_db,[client_id,loss_amount,generate_hash(client_id,loss_amount)])
            #print(f'client:{client_id},loss_amnt:{loss_amount}')
            
            return JsonResponse({"status": "success", "message": f"Client {client_id} Loss {loss_amount}"})

        except Player.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Client {client_id} not found"}, status=404)

    else:
        return JsonResponse({"status": "error", "message": "Invalid data received"}, status=400)




def success(request):
    # Get the client ID and win amount from the URL
    client_id = request.GET.get('mobile')
    win_amount = request.GET.get('win_amount')

    if client_id and win_amount:
        try:
            check_add(win_db,[client_id,win_amount,generate_hash(client_id,win_amount)])

            #print(f'client:{client_id},win_amnt:{win_amount}')

            

            return JsonResponse({"status": "success", "message": f"Client {client_id} won {win_amount}"})

        except:
            return JsonResponse({"status": "error", "message": f"Client {client_id} not found"}, status=404)

    else:
        return JsonResponse({"status": "error", "message": "Invalid data received"}, status=400)


def admin_required(user):
    return user.is_staff


def live_data(request):
     # Prepare the data for the template
    reader=read(find_file('live_data.csv'))
    games = []
    for row in reader:
        if len(row) >= 4:
            game_id = row[0]
            game_name = row[1]
            home_score = row[2]
            away_score = row[3]
            games.append({'id': game_id, 'name': game_name, 'home_score': home_score, 'away_score': away_score})
    
    return render(request, 'live_scores.html', {'games': games})


# Sample view for client profile page
def client_profile(request,ckey):
    dec_data = decrypt_web('krypton', ckey)
    mobile, balance = dec_data.split(',')
    # Assuming you have a client object with these attributes
    no_slips=len(find(slips_file,mobile))
    slips=find(slips_file,mobile)
    f_slips=0
    for f in slips:
        if f[5]=='fail':
            f_slips+=1
    #print(f_slips)
    client = {
        'mobile': mobile,
        'num_slips': no_slips,
        'failed_slips': f_slips,
        'balance': str(balance)
    }
    
    return render(request, 'profile.html', {'client': client})

def mpesa_response(request):
    data = request.body.decode('utf-8')
    datas = json.loads(data)
    print(f'mpesa response:{datas}')

def about(request):
    return render(request,'about.html')

def chatx(request):
    return render(request,'chat.html')
