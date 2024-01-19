#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import sys
import socket
from aiohttp import ClientConnectorError, ClientOSError, ServerDisconnectedError, ServerTimeoutError, ServerConnectionError, TooManyRedirects
from tqdm import tqdm
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from typing import List

#LIGHT_GREEN = '\033[92m'
#DARK_GREEN = '\033[32m'
#ENDC = '\033[0m'

redirect_payloads = [
    "//example.com@google.com/%2f..",
    "//google.com/%2f..",
]

async def load_payloads(payloads_file):
    if payloads_file:
        with open(payloads_file) as f:
            return [line.strip() for line in f]
    else:
        return redirect_payloads

def fuzzify_url(url: str, keyword: str) -> str:
    if keyword in url:
        return url

    parsed_url = urlparse(url)
    params = parse_qsl(parsed_url.query)
    fuzzed_params = [(k, keyword) for k, _ in params]
    fuzzed_query = urlencode(fuzzed_params)

    fuzzed_url = urlunparse(
        [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, fuzzed_query, parsed_url.fragment])

    return fuzzed_url

def load_urls(file_path: str) -> List[str]:
    with open(file_path) as f:
        urls = [line.strip() for line in f]
    return [fuzzify_url(url, "FUZZ") for url in urls]

async def fetch_url(session, url):
    try:
        async with session.head(url, allow_redirects=True, timeout=10) as response:
            return response
    except (ClientConnectorError, ClientOSError, ServerDisconnectedError, ServerTimeoutError,
            ServerConnectionError, TooManyRedirects, UnicodeDecodeError, socket.gaierror,
            asyncio.exceptions.TimeoutError):
        tqdm.write(f'[ERROR] Error fetching: {url}', file=sys.stderr)
        return None

async def process_url(semaphore, session, url, payloads, keyword, pbar, output_file):
    async with semaphore:
        for payload in payloads:
            filled_url = url.replace(keyword, payload)
            response = await fetch_url(session, filled_url)
            if response and response.history:
                last_location = str(response.history[-1].url)
                if last_location in ["http://google.com/","https://google.com/"]:
                    output_line = f'[FOUND] [{filled_url}] redirects to [{last_location}]\n'
                    tqdm.write(output_line)
                    if output_file:
                        with open(output_file, 'a') as f:
                            f.write(output_line)
            pbar.update()

async def process_urls(semaphore, session, urls, payloads, keyword, output_file):
    with tqdm(total=len(urls) * len(payloads), ncols=70, desc='Processing', unit='url', position=0) as pbar:
        tasks = []
        for url in urls:
            tasks.append(process_url(semaphore, session, url, payloads, keyword, pbar, output_file))
        await asyncio.gather(*tasks, return_exceptions=True)

async def main(args):
    if args.url:
        urls = [fuzzify_url(args.url, args.keyword)]
    elif args.file:
        urls = load_urls(args.file)
    else:
        print("Error: Either -u or -f must be provided.")
        sys.exit(1)

    payloads = await load_payloads(args.payloads)
    tqdm.write(f'[INFO] Processing {len(urls)} URL(s) with {len(payloads)} payloads.')

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(args.concurrency)
        await process_urls(semaphore, session, urls, payloads, args.keyword, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenRedireX: A fuzzer for detecting open redirect vulnerabilities")
    parser.add_argument('-p', '--payloads', help='file of payloads', required=False)
    parser.add_argument('-k', '--keyword', help='keyword in urls to replace with payload (default is FUZZ)', default="FUZZ")
    parser.add_argument('-c', '--concurrency', help='number of concurrent tasks (default is 100)', type=int, default=100)
    parser.add_argument('-f', '--file', help='file containing URLs', required=False)
    parser.add_argument('-u', '--url', help='single URL to test', required=False)
    parser.add_argument('-o', '--output', help='output file path')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nInterrupted by the user. Exiting...")
        sys.exit(0)
