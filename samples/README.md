Scalr APIv2 Samples
===================

This repository contains code samples for the Scalr API. An actual API client is contained within [`./api`](./api).

Using the samples
-----------------

  1. (Optional) Create a Python virtual environment to avoid installing dependencies system-wide
  2. Install the dependencies: `pip install requirements.txt` (you might need to `sudo` if you are installing system-wide).
  3. Create a credentials file: copy `credentials-sample.json` to `creds.json` and update the values there.
  4. Run the sample code: `python main.py creds.json list` and `python main.py creds.json create`. See below for more information.
 
 
Samples
-------

Two samples are includes:

  + `list` calls the Scalr API to list Roles, Images, Role Categories, and OSes.
  + `create` creates an Image and a Role, associates the Image with the Role, and then cleans up by undoing everything
    it did.
    
You can find the code for those samples under [`scenarii`](./scenarii).
