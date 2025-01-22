# Mist Org Cleanup Script

This Python script provides an **interactive, command-line** way to list and delete various **Mist** resources—such as **Sites**, **Applications**, **Networks**, **Hub (Gateway) Profiles**, and **WAN Edges**—within a specific organization. It automates API calls to Mist’s REST API endpoints based on your selections, making it easier to clean up multiple resources at once.

---

## Features

1. **Menu-Driven Interface**  
   Users can select which category (section) of resources to manage:
   - Sites
   - Applications
   - Networks
   - Hub Profiles (gateway device profiles)
   - WAN Edges

   A **“Remove All”** option (menu item) can delete **all** items in **all** categories in one command.

2. **Dynamic Deletion Paths**  
   Each resource type may require different API paths for **listing** and **deletion**.  
   For example:
   - **Sites** are listed via `/orgs/{org_id}/sites` but deleted via `/sites/{site_id}`.
   - **Hub (gateway) profiles** are listed with `/orgs/{org_id}/deviceprofiles?type=gateway` but deleted via `/orgs/{org_id}/deviceprofiles/{id}`.

3. **Configurable Authentication**  
   - Reads a local file `Token-Org.txt` containing:
     ```
     token=<your_mist_api_token>
     org_id=<your_org_id>
     ```
   - Ensures you do not hardcode credentials in the script.

4. **Failsafe Prompts**  
   - The script prompts for **confirmation** before deleting items—either selectively or all at once.

5. **Modular Design**  
   - Each “section” (e.g., Sites, Applications, Networks) is defined in a `sections` dictionary with **list** and **delete** paths.

---

## Requirements

- **Python 3.x**
- [**requests**](https://pypi.org/project/requests/) library
  ```bash
  pip install requests

##  Setup
Install Dependencies

bash
Copy
pip install requests
Create Token-Org.txt
In the same folder as the script, create a file named Token-Org.txt:

makefile
Copy
token=<YOUR_MIST_API_TOKEN>
org_id=<YOUR_ORGANIZATION_ID>
Make sure this file is excluded from version control if it contains sensitive info.

## Run the Script

bash
Copy
python your_script_name.py
The script will read your token and org ID, then show you a menu.

## Usage
When you run the script, you’ll see a menu:
Choose a section to manage:
 1. Sites
 2. Applications
 3. Networks
 4. Hub Profiles
 5. WAN Edges
 6. Remove All (All Sections)
 0. Exit
Select a number (1–5) to manage that resource:
The script lists all found items for the chosen section.
You can delete specific items by entering their index (e.g., 1,3,5) or type all to delete every item in that section.
Type exit to return to the main menu without deleting.
Select “6” to remove every resource in all sections (after a single confirmation).
Select “0” to exit.
Example Workflows
Delete a Single Site

Select 1 for Sites.
The script displays your existing sites, each with an index (1, 2, 3, …).
Enter 2 (for example) to remove the second site. Confirm “yes” to finalize.
Delete All Hub Profiles

Select 4 for Hub Profiles (gateway device profiles).
Enter all at the deletion prompt.
Confirm “yes” to remove all hub profiles returned by the listing.
Remove Everything

Select 6 (“Remove All”).
After a single “Are you absolutely sure?” confirmation, the script iterates through all sections (Sites, Applications, Networks, Hub Profiles, WAN Edges) and deletes any items found.
