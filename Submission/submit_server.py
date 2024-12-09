
# The platform Vjudge has an easier way to automate submissions
import requests
import base64
import time
import jsonlines
import os

PYTHON_LANG_ID = 41
CPP_LANG_ID = 91 # todo: find the correct language ID for C++

COOKIE_STRING="JSESSlONID=17F45R8NH1YYJ495Y57RX5G9HM2ST0F5; _ga=GA1.1.1043769253.1732838236; __gsas=ID=fce1de241db2d9b3:T=1732838237:RT=1732838237:S=ALNI_Ma8P5DuxXlDRy4uk4CbwC0maxXZlg; JSESSIONID=9255AB88AB8219DBF83C9AF532D32DAF; Jax.Q=qwen_1b_results|1ZMZ9AMCZBIO6VQHG8RVBGO573AO5B; cf_clearance=KGbcYZrNi.MsRGSK2jvQSGCUpu69aUBoi6NuedEKjVw-1732844573-1.2.1.1-qC.qQiymtdSIEAwX1Uxrqn0EGC57Xzq4024YSv57hnIvErzPz4AuMiSlFnlAlJbeZ2kjP3E_aXmeqdxQfJZFlX6fS4VsFnU5r7t9g7efamBnJANv7dhZM00fr4Doe4NLsT9nzV3EgA8iGInUH25jl0C_d16uf527TE2L7FOw87Tl_WH_Oa5Wvy6OgBwrbjjaE.gmfW9LZdx2ezxs_uMfEz1HGSyn_yi0Eio6IiofUdA9k.jnkL1Ybiol2c8eOfwisUwrGxkMJXEJGLal.T6xzpB7OLAjRQUTT4CjlhtsgaiRn8dL5ylH.gffCISK5UQhPbLYlISYBLaJ7ED2N_m1h2A4ZsX7lU.rRPZ7.rEnSiu7PPYwOe7W1kn4ATBuFqOPCmclGyexLCTaOzIrgU5F5w; __gads=ID=c246648a0e547a0b:T=1732838236:RT=1732845063:S=ALNI_MZD1A0dey3orjNFnRsTLEGFH-mi6Q; __gpi=UID=00000fa21c01df6c:T=1732838236:RT=1732845063:S=ALNI_MZ9mUTvLkt5MoQu5AM1vJJvCYA0Dw; __eoi=ID=807a08723a90e8ee:T=1732838236:RT=1732845063:S=AA-AfjZ97X5E72kOKZBLqN3H-rSs; FCNEC=%5B%5B%22AKsRol-bGZLupHg-NsqOAgf9Pr_-Wcy3Q3vtapKRJblL9lmrEYowWcEtgqCkB1-xrEeCfxkjdPOc-KRf6J_RMshSIzYzEpYeKtB9zoZ8-Lyh_3GqEKerfDd-r-wb3oKdaV3FF8ZvxwQIwImTdxH4HGaXOMnxwmrP6w%3D%3D%22%5D%5D; _ga_374JLX1715=GS1.1.1732838235.1.1.1732845234.44.0.0"

#COOKIE_STRING = '_ga=GA1.1.1678087588.1677102754; _ga_374JLX1715=GS1.1.1698286289.4.0.1698286289.60.0.0; JSESSlONID=1PXHI4E4QR2MYNS67G5955PKAQVA61VI; JSESSIONID=3A2A86C92E444B3CBD2A04995347BD76; cf_clearance=9DDZV11KWqOHUjFmcyn652VIC3YPP5VSDr63rxe_U0w-1732821959-1.2.1.1-fQAMQUieIrt9s1phf3dw8ndN6Cop5JquGsrmPM7SuNoMPK7vQUEqA_7P0M9i4IzvMIgYG0qkuyvmffavEFUW2y84I8qw7ebW0okw2f4H.eG_3a4Uyxc7tqSgKMHZe_vN.oWnvcesO3Ssjz_4SMtkBJpxhJMVKUGYbUGN9wWW_TEejp8dMuIl.DWYy8PTySBRc6ksIXT03efx_ecO9CIjnfk3GkKUbN9mtqNlAP1MQnYmdbNihdUADvczmXXO1AHTwxhmAscF8Ef08of1MRdHbcQUsXTJHOXMZR9ycqgSfqJXPtoZHQFkA1f2dFs8Eb7Yvz6HTTjHuw7Y5tx5hFggM13rQwMX0Fy8bYkBfysrj7N1j5HMzsyOnSLG9emyl8OzKCDFv7KR8sDojjL0xl_8gg; Jax.Q=apoli99|AOFMLTIGF9H1CGLGSQ5Z1I5OTJCC9H'

# COOKIES = [ 
    # ['JSESSlONID', '1PXHI4E4QR2MYNS67G5955PKAQVA61VI'],
    # ['JSESSIONID', '60ACDB4D523E5B59E9D7F79818A5ECAD'],
    # ['Jax.Q', 'test_iser19|I0Y785G3CMLJTPHR172WJUJXTYHGK4'],
    # ['_ga', 'GA1.1.1678087588.1677102754'],
    # ['_ga_374JLX1715', 'GS1.1.1698286289.4.0.1698286289.60.0.0'],
    # ['cf_clearance', 'rbYWxaPIw8KhUH5UI_OHQPQ60.v5gahuD1vzvZHpiEI-1730251953-1.2.1.1-70TNqqLrMdCSFS6YD75Hq_KGYwMDR8jH9cWgBvBfIH0QpLRqP3NRDLlBECNEiAssMItSOIUjOaq9sOGDgo1kptW80CMCcl4ZwKgXGI9iNNTT5CV6_2farhSm7e_Y1Xu1y5RE0wg0w5R02eofSuTQyuHLuduFWdlo.yZ8UFPK_8L_POziTrE3ccVgV49AWJejE2DvQrAY9FHTckq1ixNzYWBJ37_py7HAtHfwS5AhjitFxREPGmofe45PcFprgq5gBMXqFldkbqcsniAYA8MJ9ZxyUapKaFtIaT2zChkcIjSK5_G4hV7EHO3Ae9fESsuqQeth10Rzu6OsuH0i8kVeHaaol45t210ogxG15rDNbukkQk4vyog4lrUljXu5dggPHoYINIdPDJ3YUC7hq5yKLQ']
# ]

USERNAME = 'qwen_1b_results'

def extract_problem_id(codeforces_url):
    # Returns problem ID given a Codeforces URL
    # Example: https://codeforces.com/contest/1339/problem/A -> 1339A
    parts = codeforces_url.split('/')
    contest_id = parts[-2]
    problem_id = parts[-1].split('.')[-1].upper()
    for c in contest_id:
        if not c.isdigit():
            raise ValueError("Invalid contest ID")
    if not problem_id[0].isalpha():
        raise ValueError("Invalid problem ID")
    
    return f"{contest_id}{problem_id}"


from urllib.parse import quote
def to_url(solution):
    return quote(solution)

def get_content(problem_id, language_id, solution):
    content = r'method=0&language={language_id}&source='
    # Encode the solution using Base-64 and replace special characters
    content += base64.b64encode(to_url(solution).encode('utf-8')).decode('utf-8')
    content += f'&oj=CodeForces&probnum={problem_id}'
    return content


def submit(problem_id, solution):
    # heuristic guess for language ID, can be explictely set later
    lang_id = (PYTHON_LANG_ID if (solution.find('#include') == -1) else CPP_LANG_ID)
    content = get_content(problem_id, lang_id, solution)


    content = {
        'method': '0',
        'language': lang_id,
        'open': '1',
        'source': base64.b64encode(to_url(solution).encode('utf-8')).decode('utf-8'),
        'oj': 'CodeForces',
        'probNum': problem_id
    }

    vjudge_url = f'https://vjudge.net/problem/CodeForces-{problem_id}'
    headers = {
        'Accept' : r'*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '; '.join([f'{k}={v}' for k, v in COOKIES]),
        'Cookie': COOKIE_STRING,
        'Origin': 'https://vjudge.net',
        'Priority': 'u=1, i',
        'Referer': vjudge_url,
        'Sec-Ch-Ua': r'"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': r'"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
        
    debug_raw_message = False
    if debug_raw_message:
        req = requests.Request('POST', 'https://vjudge.net/problem/submit', headers=headers, data=content)
        prepared = req.prepare()

        # Print the raw request details
        print(f"URL: {prepared.url}")
        print(f"Headers: {prepared.headers}")
        print(f"Body: {prepared.body}")
        # print(to_url(solution))
        return
    
    response = requests.post('https://vjudge.net/problem/submit', headers=headers, data=content)

    if response.status_code != 200:
        print(response.status_code)
        raise Exception(f"Failed to submit solution: {response.text}")
    print('Submitted...')
    time.sleep(60)

        
def check_status(problem_id):
    # Check the submission status of the latest submission; t
    # TODO: This doesn't work and I'm going to have to change
    # my approach quite a bit to fix it. Planning on trying to 
    # give Vjudge a CF cookie and then just checking status on CF.
    # If Vjudge keeps flagging the program, I might have to interface
    # with CF directly.
    url = f'https://vjudge.net/status#un={USERNAME}&OJId=CodeForces&probNum={problem_id}&res=0&language=&onlyFollowee=false'
    print(url)


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)
    response.raise_for_status()
    
    html_content = response.text

    print(html_content)

    def get_pos(s):
        res = html_content.find(s)
        if res == -1: return 2 ** 30
        return res
    
    accepted_pos = min(get_pos('accepted even'), get_pos('accepted odd'))
    pending_pos = min(get_pos('pending processing even'), get_pos('pending processing odd'))
    failed_pos = min(get_pos('failed even'), get_pos('failed odd'))
    if pending_pos < accepted_pos and pending_pos < failed_pos:
        return 'pending'
    if accepted_pos < failed_pos:
        return 'accepted'
    return 'failed'
    


url = 'https://codeforces.com/contest/2021/problem/A'

solution_py = '\n'.join([
    'for _ in range(int(input())):',
    '    n = int(input())',
    '    a = list(map(int, input().split()))',
    '    while len(a) > 1:',
    '        a.sort()',
    '        s = a[0]',
    '        a = a[1:]',
    '        a[0] = (a[0] + s) // 2',
    '    print(a[0])'
])

solution_cpp = '\n'.join([
    '#include <bits/stdc++.h>',
    'using namespace std;',
    'int main() {',
    '    int t;',
    '    cin >> t;',
    '    while (t--) {',
    '        int n;',
    '        cin >> n;',
    '        vector<int> a(n);',
    '        for (int i = 0; i < n; i++) {',
    '            cin >> a[i];',
    '        }',
    '        while (a.size() > 1) {',
    '            sort(a.begin(), a.end());',
    '            int s = a[0];',
    '            a.erase(a.begin());',
    '            a[0] = (a[0] + s) / 2;',
    '        }',
    '        cout << a[0] << endl;',
    '    }',
    '    return 0;',
    '}'
])

url_list = []
with jsonlines.open('./easy_problems.jsonl') as reader:
        for obj in reader:
            url_list.append(obj['url']) 


prompt_dirs = ['./prompt_1_sanitized', './prompt_2_sanitized', './prompt_3_sanitized']
model = '/qwen_1b_results/'
for root_dir in prompt_dirs:
    for i in range(22):
        print(root_dir,  i)
        with open(root_dir + model + str(i) + '.txt', 'r') as handle:
            solution_py = handle.read()
        problem_id = extract_problem_id(url_list[i])
        submit(problem_id, solution_py)  # Submit the solution
    

#submit(problem_id, solution_cpp)  # Submit the solution

exit(0)


time.sleep(5)  # Wait for a while before checking the status

while check_status(problem_id) == 'pending':
    print('Pending...')
    time.sleep(5)

print('Final Status:', check_status(problem_id))  # Check final status
