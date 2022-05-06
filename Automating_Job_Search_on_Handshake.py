## Import dependent packages
import smtplib
import threading
import time
from email.mime.text import MIMEText
import redis
import requests

### Create a request header
### The request header is copied from the website after logging in
headers ={
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Cookie': '_biz_uid=091fc61cf84f464cd1361db433dae24e; _ga=GA1.2.162211769.1651559894; _gid=GA1.2.1228509986.1651559894; _gcl_au=1.1.1882419296.1651559894; _mkto_trk=id:390-ZTF-353&token:_mch-joinhandshake.com-1651559893926-38698; ajs_anonymous_id=%22d40193dc-f060-441b-b47f-59feb45f3645%22; _clck=1rxu0n0|1|f15|0; _uetsid=9b9d65b0caab11ecb4a9b1e4234fde44; _uetvid=9b9d8390caab11ec8dfde7b0b68dea58; _hjSessionUser_1832914=eyJpZCI6IjU2M2EyMGEyLWMwMjQtNTgzMC1hMDQ2LWZkYWQ0MTc0YjBiZiIsImNyZWF0ZWQiOjE2NTE1NTk4OTQzNTIsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1651559971163.1149207937; _clsk=zwmmsh|1651559972509|2|1|l.clarity.ms/collect; _biz_nA=4; _biz_flagsA=%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%2C%22Mkto%22%3A%221%22%7D; _biz_pendingA=%5B%5D; __pdst=eaefe2a0718c4b70b537343b3def1287; hss-global=eyJhbGciOiJkaXIiLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIjoiSldUIn0..WKoQh7LbHi4-Wj--vQ_K1Q.26SUf0rVKpAS_8ozVvgHRTlz14ND3KnI-LopdTrmQyUf-xJmwSpyP703I8tPdWUNybpXE5SjhXT7kCc4QeNvD64mQnbYYJ6KHRxG25_qDwEeyulm-ezwjDPoSyxXBONRvDqwmcpo72-kfoV2RbjZgj4UzeLd-Xvql1OG_LhbkyqvjUW2wyeVjy0CdRjj91H3zRKXAAaPsJHpN9kqUKHzD4iEUjvWg3sf4TBnW47lxRiQHO7slocLF9rivxwEhyvH-PjQZ-SeENH3GVFuQP8Ej8qPVfBUcVSWe7c_rghWZr4_AYO7Iccy8ZU9ufsRIXvsrUqC5Xel_16wQ76YSuy2d3dRodu495vpdeM4sm4fffxvrxQlVCrhE7dA9LM-BxSD.HG5A8JuIlUzhzGzWAWuQVskvfWccG3VVUCjJdLJXiAs; ajs_user_id=10432370; production_js_on=true; production_10432370_incident-warning-banner-show=%5B%5D; _gat=1; _gat_schoolTracker=1; _gat_UA-58165706-1=1; outbrain_cid_fetch=true; request_method=POST; _trajectory_session=YUdJdWx5aG5CK3RZcytQaGRQaURVeFZ2ZXNZSmx0eW1tbzVKVy8zR21CcnRpTU53Uk84ZVRTNHUyNlJsWVRHQlRxdXhrR1hqRi9QRWswWDFoWCtERkZQUVptK29tbDlDeTR6cmNsRENBNG1VSmkxREtHTmlZNzVLWUtvQ1QzUUZzaUlsOC9OQnR1bXNrZWkwd1EveitKdUp3UERBRk5tZjdEa3dzRS9zL2EzZitScWxvd2pKQ0V4a3ZvclVSRE52Y0plamJWRXllbUw5clE3RjZvQ3QrQT09LS1sQjd6MkRZSU85N3dQT0QwSWFiUDVRPT0%3D--e5d9eb22ab71afe4affbb6a54db7195381ccd68d',
'Host': 'temple.joinhandshake.com',
'Referer': 'https://temple.joinhandshake.com/stu/postings?page=1&per_page=25&sort_direction=desc&sort_column=created_at',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
'X-CSRF-Token': 'WI/cgkA+3rxtZbhD8XDqOpaDa7jeJJXwATfixlsH8cNJygW2jrxcn3AU2DHoDewG7U26BbaXKpo06B/K1f71og==',
'X-Requested-With': 'XMLHttpRequest'
}
### Subscribe to posts with keywords
job_key = 'assistant'
### Push frequency (Units s)
intever_search = 60*60




## This function is used to get the latest job data
def search_keyword(job_key):
    ## Display the network address of the latest post
    url = f'https://temple.joinhandshake.com/stu/postings?category=Posting&ajax=true&including_all_facets_in_searches=true&page=1&per_page=25&sort_direction=desc&sort_column=created_at&' \
          f'query={job_key}&_=1651572199134'

    ## An endless loop initiates a network request
    ## Normal requests exit the loop, and exception requests relink
    while True:
        try:
            ## Specify the request URL, request headers, request timeout period
            page = requests.get(
                url,
                headers=headers,
                timeout=(3,4)
            )
            ## Thread sleeps 0.7s
            time.sleep(0.7)

            ##Returns json text
            return page.json()
        except Exception as e:
            print(f"> Network exception : {e} ")
            ##The exception request thread sleeps for 2s and then retries
            time.sleep(2)


def get_newjobs(job_key):
    ## Create a redis database link
    ## Redis is used to store collected post IDs
    rinset = redis.Redis(host="47.111.108.89",password='961948438', port=6379, db=9)

    ## If the key job_id does not exist in redis
    if not rinset.exists('job_id'):

        ## Get the latest job data by keywords
        response_job = search_keyword(job_key)

        ## Gets the list of jobs in the response text
        engine_jds = response_job.get("results")

        ## Iterate through each post and write the id to the redis database
        for current_job in engine_jds:
            ##  Insert post id
            rinset.sadd('job_id', current_job.get("job_id"))
            ## Print the log
            print(f">>> insert database；{current_job.get('job_id')}")
        return []

    else:
        ## If the key job_id exists in the database

        ## Get the latest job data by keywords
        response_job = search_keyword(job_key)
        ## Gets the list of jobs in the response text
        engine_jds = response_job.get("results")

        ##Define a list of new positions
        new_jobs = []
        for current_job in engine_jds:
            ## If the post id exists in the database
            ## Continue iterating
            if rinset.sismember('job_id', current_job.get("job_id")):
                job_id = current_job.get("job_id")
                job_name = current_job.get("job_name")
                employer_name = current_job.get("employer_name")
                updated_at = current_job.get("updated_at")
                ## Indicate that the current position is not a new position
                text = f">>> No changes sent Old posts: {job_id} {job_name} {employer_name} {updated_at}"
                print(text)
                continue
            ## Add new positions to the list
            new_jobs.append(current_job)
            ## Insert the current job id into the database redis
            rinset.sadd('job_id', current_job.get("job_id"))
        ## Return to the list of new positions
        return new_jobs





def dowork(job_key):
    ## Thread execution logs
    print(f'\n A task is being executed：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    try:

        ## Get a new job for the current keyword
        new_jobs = get_newjobs(job_key)

        ###Iterate through each post dictionary to extract the required values
        for current_job in new_jobs:
            ## Post id
            job_id = current_job.get("job_id")
            ## Job nickname
            job_name = current_job.get("job_name")
            ## employer_name
            employer_name = current_job.get("employer_name")
            #updated_at
            updated_at = current_job.get("updated_at").split(".")[0]
            # Job description
            job_desc = current_job.get("job").get("text_description")
            ## Post update time
            timesamp = time.mktime(time.strptime(updated_at,'%Y-%m-%dT%H:%M:%S'))

            ## If the job update time and the current time difference is more than 10 times the last push
            if time.time() - timesamp > intever_search * 10:
                ## Cancel the push
                print(f">>> Post update time is far away Cancel sending {job_id} {job_name} {employer_name} {updated_at}")
            else:
                ##  Otherwise, the log is printed and pushed
                job_url = f'https://temple.joinhandshake.com/stu/jobs/{job_id}?ref=preview-header-click'
                print("*" * 50)
                print("\n\n")
                print(f">>> Pushing {updated_at}  {job_id} {job_name} {employer_name} {job_url}")
                aend_email(job_id,job_name,employer_name,updated_at,job_url,job_desc)
                print("\n\n")
                print("*" * 50)


    except Exception as e:

        print(f">>> Execution exception: {e}")



def aend_email(job_id,job_name,employer_name,updated_at,job_url,job_desc):

    ## Defines the text pushed
    content = """
    job_id：%s
    job_name：%s
    employer_name：%s
    updated_at：%s
    job_url：%s
    job_desc：%s
    """ % (job_id,job_name,employer_name,updated_at,job_url,job_desc)

    ## Pusher mailbox
    msg_from = '961948438@qq.com'
    ##Pusher protocol password, non-email password
    passwd = 'ijomqjqxetxabcjf'
    ## Recipient mailbox
    msg_to = '961948438@qq.com'

    ## Define the context
    subject = "new-job"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        ## Log in and push a new post
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        result = s.sendmail(msg_from, msg_to, msg.as_string())
        print(f">>>> Push the results： {result}")
    except Exception as e:
        print(f">>> Failed to send：{e}")




if __name__ == "__main__":

    ## Perform tasks on a regular basis: target
    ## The parameter job_key is the keyword used to search for jobs
    ## The purpose of multithreaded execution is to prevent the main thread from getting stuck
    while True:

        ### Create thread `th`
        th = threading.Thread(target=dowork,args=(job_key,))
        ### Thread `th` of execution
        th.start()
        ## The main thread sleeps for a specified amount of time
        time.sleep(intever_search)
