# =================================================================
#
# Authors: Ben Webb <benjamin.miller.webb@gmail.com>
#
# Copyright (c) 2022 Ben Webb
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import grequests
import time
import sys

def main(argv):
    start = int(argv.pop(0))
    stop = 2938143 if argv[0] == "-1" else int(argv.pop(0))
    step = 50 if len(argv) == 0 else int(argv.pop())
    print(start, stop, step)
    start_time = time.time()
    send_request(start, stop, step)
    print(f"End Time: {time.time() - start_time}")

def send_request(startindex, endindex, step):
    step = min(endindex-startindex, step)
    urls = make_urls(startindex, step)
    rs = (grequests.get(u) for u in urls)
    start_time = time.time()
    print(grequests.map(rs))
    print("%.3f |" % (time.time() - start_time))

    if (startindex < endindex):
        send_request(startindex+step, endindex, step)
    
def make_urls(start, step):
    base_url = "https://merit.internetofwater.app/processes/river-runner/execution?id={}"
    return [base_url.format(i) for i in range(start, start+step)]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: {} <start_ogc_fid> <end_ogc_fid> <group_size>'.format(sys.argv[0]))
        sys.exit(1)
    
    main(sys.argv[1:])
