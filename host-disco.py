from scapy.layers import l2
import argparse
import logging

def arp_scan(ip_range):
    """
    Perform an ARP scan on the given IP range.
    """
    try:
        print(f"Starting ARP scan on {ip_range}...")
        ans, _ = l2.arping(ip_range)
        print(f"ARP scan completed for {ip_range}")
        print(f"Number of devices found: {len(ans)}")
    except Exception as e:
        logging.info(f"Error during ARP scan: {e}")
        return None
    return ans

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.CRITICAL)

    # Add a StreamHandler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Set up argument parser
    parser = argparse.ArgumentParser(
        prog='host-disco',
        description='This is a homemade host discovery tool that uses arp-scanning',
        epilog='Thank you for using this tool! If you have any suggestion or feedback, let me know :)'
    )

    parser.add_argument('-n', '--network', help="The Network to scan")
    parser.add_argument("-v", "--verbose", action = "store_true", help="Enable verbose output")

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    if args.network != None:
        # Perform ARP scan
        ans = arp_scan(args.network)
        if ans:
            for sent, received in ans:
                print(f"IP: {received.psrc}, MAC: {received.hwsrc}")
        else:
            logger.info("No devices found.")



