# Robot Framework Results Email

Send email with robotframework result (Suite, Test, Keyword and Execution time)

---

*How it Works:*

1. Read output.xml file using robotframework API
2. Get Suite, Test Case, Keyword and Execution time
3. Sends email to specified users 

---

*How to use in project:*

1. Download __robotemail.py__ from here [link](https://github.com/adiralashiva8/robotframework-metrics/releases/download/v3.0/robotemail.py)

    > Repo has some extra files (.html and .xml for testing) - I suggest to download from link

2. Copy __robotemail.py__ file to project

3. Execute __robotemail.py__ file

    > Case 1: robotemail.py is copied where output.xml is available

    ```
    python robotemail.py
    ```

    > Case 2: Specify output.xml file path. (When .xml is same)

    ```
    python robotemail.py -inputpath .\Result\
    ```
    
    > Case 3: Specify file name. (When .xml file name is altered)

    ```
    python robotemail.py -inputpath .\Result\ -output voutput.xml
    ```
    
5. Email will be sent to mentioned users

---

 __SAMPLE EMAIL__

 ![Screenshot](sample.jpg)

 ---

*How to Specifiy EMAIL recepients*
 - In __robotemail.py__ file add specific to, from, subject and email server info
    ```
    server = smtplib.SMTP('smtp.gmail.com:587')
    msg = email.message.Message()
    msg['Subject'] = 'Automation Status'

    sender = 'me@gmail.com'
    recipients = ['user1@gmail.com', 'user2@yahoo.com','user3@hotmail.com']

    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    password = "xxxxxxxxxxxxxxxxxx"
    ``` 
---

*How to Ignore Library Keywords in EMAIL*
 - In __robotemail.py__ file add specific library keywords to tuple __ignore_library__ to ignore in report
 - In EMAIL, keywords with type value 'for' and 'foritem' are ignored
 - Following library keywords are ignored in EMAIL stats
    ```
    ignore_library = [
     'BuiltIn',
     'SeleniumLibrary',
     'String',
     'Collections',
     'DateTime',
    ] 
    ``` 
---
    >  STAR repo to appreciate
---