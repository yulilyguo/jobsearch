
0. Tools: Redis Database & Python



1. Import dependent package

    import smtplib   
    import threading  
    import time  
    from email.mime.text import MIMEText   
    import redis  
    import requests  

2. Define variable

    headers =  ...     ##Create the headers
    job_key = 'assistant'  ### Subscribe to job keywords
    intever_search = 60*60  ### Crawl time interval


3.  Creating a timed task

        while True:

        ### Create thread `th`
        th = threading.Thread(target=dowork,args=(job_key,))
        ### Thread `th` of execution
        th.start()
        ## The main thread sleeps for a specified amount of time
        time.sleep(intever_search)


4.  Execute the dowork function to start the main task



5.  Call the get_newjobs function in the dowork function to obtain new jobs



6.  Launch the network in the get_newjob function, get a list of all jobs, and then compare the list  of new jobs obtained and return it to the dowork function


7. Extracting job fields that have not been pushed

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

8. No new posts pushed to the recipient (filter time first, too long not pushed)

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


