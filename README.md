# ISE - Device Access Policy Automation
This prototype is to automate ISE Device Access Policy (TACACS+) for internal users, by changing their identity groups programmatically using ISE APIs. Note: The policy rules must be setup in ISE in advance following the guide in the attached PPT


## Contacts
* Rami Alfadel

## Solution Components
* Cisco ISE (Identity Services Engine)
* TACACS+ (Device Access Administration)
* Python

### High-level Overview

![/IMAGES/overview.png](/IMAGES/overview.png)

A video showing a sample run of this prototype: [ISE - Device Access Policy Automation](https://youtu.be/X6eBdJmDp1I)

## Installation/Configuration
 1. Make sure you have [Python](https://www.python.org/downloads/) installed
 
 2. Clone this Github repository into a local folder:  
   ```git clone [add github link here]```
    - For Github link: 
        In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
        ![/IMAGES/giturl.png](/IMAGES/giturl.png)
    - Or simply download the repository as zip file using 'Download ZIP' button

 3. Access the downloaded folder:  
   ```cd <folder_path>```

 4. Load up the required libraries from *requirements.txt* file:  
   ```pip install -r requirements.txt```
 
 5. Check that you have enabled [ISE ERS (External RESTful Services) APIs](https://developer.cisco.com/docs/identity-services-engine/3.0/#!setting-up) for the environment you're working on.
 
 6. Configure the configuration variables in ```config.py``` file:
      
    1. Set up the connectivity to ISE instance:
          ```python
          ''' Update the below variable to have ISE connection variables '''
          HOST = 'https://<ise_address_here>'
          USERNAME = '<username_here>'
          PASSWORD = '<password_here>'
          ```

## Usage

There can be two ways to change the user's identity group with this prototype:  
### Using the terminal/console prompt to change the user's group:
 1. By running the script *change_group.py*:    
        ```python change_group.py```
 2. It will read the list of identity groups in ISE, prints them as list of Name & ID, and asks for the user to select the id of the desired group:  
  ![/IMAGES/change_group_prompt.png](/IMAGES/change_group_prompt.png)


 ### Using the sample web application UI to request a change to the user's group:
 1. Initiate the Flask application settings:  
   ```export FLASK_APP=app.py```  
   ```export FLASK_ENV=development```

 2. Start the Flask application:  
   ```flask run```

 3. Open the hosted web page in your browser:  
    (Default: [localhost:8000](localhost:8000))

    - This prototype will read the list of [Internal Users](https://www.cisco.com/c/en/us/td/docs/security/ise/2-1/admin_guide/b_ise_admin_guide_21/b_ise_admin_guide_20_chapter_01101.html#ID24) and the list of [Identity Groups](https://www.cisco.com/c/en/us/td/docs/security/ise/2-1/admin_guide/b_ise_admin_guide_21/b_ise_admin_guide_20_chapter_01101.html#concept_E108A3362A784FC2A8F0C5FACBACB948) found in ISE.

 4. A selected user (the latest user found, can be changed at app.py: lines 58-60) will be asked to select a group to join from a dropdown list:  
 ![/IMAGES/dropdown_list.png](/IMAGES/dropdown_list.png)

 5. Once the request is submitted, the web interface will show a confirmation:  
 ![/IMAGES/request_submitted.png](/IMAGES/request_submitted.png)

 6. In the application's backend, the request will be received and a y/n prompt will be shown to the admin, asking if the request should be approved:  
 ![/IMAGES/admin_approval.png](/IMAGES/admin_approval.png)
     - This can be integrated with: [Webex chatbot](https://developer.webex.com/docs/bots#responding-to-events), email notificiation, another web application for approval, etc..

 7. If the request was approved, the user's group will be changed as requested. Utilizing: [ISE Rest APIs - User Modification](https://www.cisco.com/c/en/us/support/docs/security/identity-services-engine/216543-ise-identity-group-user-creation-and-mo.html)

 8. For device access privileges to take effect, a certain [policy sets](https://www.cisco.com/c/en/us/td/docs/security/ise/2-4/admin_guide/b_ISE_admin_guide_24/m_configure_and_manage_policies.html) must be setup in ISE in advanced.
     - You can follow the instructions provided in tha attached PowerPoint slide: [Policy_Setup.pptx](/Policy_Setup.pptx)
     - Or you can follow this sample lab intructions for setting up TACACs+ as the device administration AAA server: [ISE - Sandbox Lab Guide: Device Administration (TACACS)](https://community.cisco.com/t5/security-documents/dcloud-ise-sandbox-lab-guide-device-administration-tacacs/ta-p/3930973)

## More useful resources

 - [ISE - ERS API Examples](https://community.cisco.com/t5/security-documents/ise-ers-api-examples/ta-p/3622623)
 - [ISE - CSRF(Cross-Site Request Forgery)](https://www.cisco.com/c/en/us/td/docs/security/ise/3-0/admin_guide/b_ISE_admin_3_0/b_ISE_admin_30_basic_setup.html#task_59D6282675A843C7AAAA7DF988F63DE8)
 - [ISE - TACACS+ Time of day policy](https://community.cisco.com/t5/network-access-control/ise-tacacs-time-of-day-policy/td-p/3525066)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.