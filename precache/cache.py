import grequests
import time

def main():
    start_time = time.time()
    send_request(1000, 1500)
    print(f"End Time: {time.time() - start_time}")

def send_request(startindex, endindex, step=2):
    step = min(endindex-startindex, step)
    urls = make_urls(startindex, step)
    rs = (grequests.get(u) for u in urls)
    start_time = time.time()
    print(grequests.map(rs))
    print("%.3f |" % (time.time() - start_time))

    if (startindex < endindex):
        send_request(startindex+step, endindex)
    
def make_urls(start, step):
    base_url = "https://merit-nldi.internetofwater.app/processes/river-runner/execution?id={}"
    return [base_url.format(i) for i in range(start, start+step)]

if __name__ == "__main__":
    main()
