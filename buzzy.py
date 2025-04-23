## This is a homey local file inclusion test script
## the goal of this script is to identify existent paths 
## from which configurations can be obtained
## This script is based on the working way of wfuzz
## thus its name
import logging
import requests
import urllib3
import validators
import argparse

# Ignore insecure request warning
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

def url_validator(url):
    if "=BUZZ" in url:
        if validators.url(url):
            logger.info("Yeyyyy, the url is valid")
            return True
        else:
            print("Invalid url :(")
    else:
        print("Please input a BUZZ")

def _send_request(clean_url):
    response = requests.get(clean_url, verify=False)
    status = str(response.status_code)
    content = response.text
    number_of_characters = len(content)
    number_of_words = len(content.split())
    return status, number_of_characters, number_of_words

def search_paths(url, wordlist, ignore_status = None, ignore_chars = None, ignore_words = None):
    print("Checked string -- Status -- Char count -- Word count")
    with open(wordlist,'r') as file:
        wordlist = file.read().splitlines()
    for word in wordlist:
        url_clean = url.replace("BUZZ", word)
        logger.debug("This is the url: ", url_clean)
        status, chars, words = _send_request(url_clean)
        if status == ignore_status or str(chars) == ignore_chars or str(words) == ignore_words:
            continue
        else:
            print(word, " -- ", status, " -- ", str(chars), " -- ", str(words))


if __name__ == "__main__":
    print(r"""\
                .' '.            __
       .        .   .           (__\_
        .         .         . -{{_(|8)
jgs       ' .  . ' ' .  . '     (__/
            
    
    """)
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
    parser.add_argument('-w', '--wordlist-path', help = "The Wordlist path to scan")
    parser.add_argument('-hs', '--hide-status', default = 0, help = "The status code you may want to hide")
    parser.add_argument('-hc', '--hide-chars', default = 0, help = "The number of chars you may want to hide")
    parser.add_argument('-hw', '--hide-words', default = 0, help = "The number of words you may want to hide")
    parser.add_argument("-v", "--verbose", action = "store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    
    if url_validator(args.url):
        search_paths(args.url, args.wordlist_path, args.hide_status, args.hide_chars, args.hide_words)

    else:
        print("Please input an url and a buzz buzz place")

