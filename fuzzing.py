## HTTP Header Fuzzing
## will target GET and POST requests

## will target the following host headers
## - User-agent
## - Referer
## - Authorization
## - X-Forwarded-For

import requests
import base64
import logging
import argparse

def post_creds(url, format_call, user, password):
    payload = { "username" : user, "password" : password}
    if format_call == "json":
        request = requests.post(url, json=payload)
    else:
        request = requests.post(url, data=payload)
    
    status = str(request.status_code)
    content = request.text
    if "invalid" in content.lower() or "error" in content.lower() or "incorrect" in content.lower():
        print("Login Failed Marker Detected")
    if "welcome" in content.lower() or "dashboard" in content.lower():
        print(">> POSSIBLE SUCCESS <<", user, password)
    number_of_characters = len(content)
    number_of_words = len(content.split())
    print("NUMBER OF WORDS", number_of_words)
    logger.debug(f"HTTP response: {content}")

    return status

def authorization_fuzz(url, user, password):
    user_pass = f"{user}:{password}"
    encoded_bytes = base64.b64encode(user_pass.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")

    header = {"Authorization" : f"Basic {encoded_str}"}
    request = requests.post(url, headers = header)
    status = str(request.status_code)
    content = request.text
    if "Invalid" in content or "error" in content.lower():
        print("Login Failed Marker Detected")
    if "Welcome" in content or "dashboard" in content.lower():
        print(">> POSSIBLE SUCCESS <<", user, password)
    number_of_characters = len(content)
    number_of_words = len(content.split())
    logger.debug(f"HTTP response: {content}")
    return status

def user_agent_fuzz(url, string):
    headers = {'user-agent': string}
    request = requests.get(url, headers=headers)
    status = str(request.status_code)
    content = request.text
    number_of_characters = len(content)
    number_of_words = len(content.split())
    logger.debug(f"HTTP response: {content}")
    print(f"HTTP response: {content}")

    return status

def run_post_creds(url, format_call, password_list, user=None, user_list=None):
    print("URL -- USER -- PASSWORD -- STATUS")
    if type(user) == str:
        with open(password_list,'r') as file:
            password_list = file.read().splitlines()
        for word in password_list:
            status = post_creds(url, format_call, user, word)
            print(url, user, word, status)
        return True
    if type(user_list) == str:
        with open(user_list, 'r') as file:
            user_list = file.read().splitlines()
        for username in user_list:
            with open(password_list,'r') as file:
                password_list = file.read().splitlines()
            for word in password_list:
                status = post_creds(url, format_call, username, word)
                print(url, username, word, status)
        return True

def run_auth_fuzz(url, password_list, user=None, user_list=None):
    print("URL -- USER -- PASSWORD -- STATUS")
    if type(user) == str:
        with open(password_list,'r') as file:
            password_list = file.read().splitlines()
        for word in password_list:
            status = authorization_fuzz(url, user, word)
            print(url, user, word, status)
        return True
    if type(user_list) == str:
        with open(user_list, 'r') as file:
            user_list = file.read().splitlines()
        for username in user_list:
            with open(password_list,'r') as file:
                password_list = file.read().splitlines()
            for word in password_list:
                status = authorization_fuzz(url, username, word)
                print(url, username, word, status)
        return True

def run_agent_fuzz(url, agent_list):
    print("URL -- USER-AGENT -- STATUS")
    with open(agent_list, 'r') as file:
        agent_list = file.read().splitlines()
    for agent in agent_list:
        status = user_agent_fuzz(url, agent)
        print(url, agent, status)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.CRITICAL)

    # Add a StreamHandler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    parser = argparse.ArgumentParser(
        prog='buzzy',
        description='This is a homemade Fuzzing tool that uses a Wordlist to find possible LFI vulnerabilities\n This tool is based on wfuzz, thus the name. You have to introdude BUZZ in the place you want to fuzz',
        epilog='Thank you for using this tool! If you have any suggestion or feedback, let me know :)'
    )

    parser.add_argument('-u', '--url', help="The URL to scan, including the place to BUZZ")
    parser.add_argument('-p', '--password-list-path', help = "The Password Wordlist path to scan")
    parser.add_argument('-U', '--user', help = "The user to test against")
    parser.add_argument('-ul', '--user-list-path', help = "A user list to test with passwords, this will take longer")
    parser.add_argument('-ual', '--user-agent-list-path', help = "User agent list")
    parser.add_argument('-f', '--format', help = "JSON")
    parser.add_argument("-v", "--verbose", action = "store_true", help="Enable verbose output")

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
    
    if args.user_agent_list_path is not None:
        run_agent_fuzz(args.url, args.user_agent_list_path)
    
    # Handle post credentials fuzzing
    if args.password_list_path is not None and args.format is not None:
        if args.user is not None:
            run_post_creds(args.url, args.format, args.password_list_path, user=args.user)
        elif args.user_list_path is not None:
            run_post_creds(args.url, args.format, args.password_list_path, user_list=args.user_list_path)
    
    # Handle authorization fuzzing
    if args.password_list_path is not None and args.format is None:
        if args.user is not None:
            run_auth_fuzz(args.url, args.password_list_path, user=args.user)
        elif args.user_list_path is not None:
            run_auth_fuzz(args.url, args.password_list_path, user_list=args.user_list_path)
