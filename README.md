# api-delete

Mist Org Cleanup Script
This Python script provides an interactive, command-line way to list and delete various Mist resources—such as Sites, Applications, Networks, Hub (Gateway) Profiles, and WAN Edges—within a specific organization. The script automates API calls to Mist’s REST API endpoints based on your selections, making it easier to clean up multiple resources at once.

Features
Menu-Driven Interface

Users can select which category (section) of resources to manage:
Sites
Applications
Networks
Hub Profiles
WAN Edges
A special “Remove All” option (menu item) will delete all items in all categories in a single command.
Dynamic Deletion Paths

Each resource type may require a different API path for listing and deletion.
For example, Sites are listed via /orgs/{org_id}/sites but deleted via /sites/{site_id}.
Hub Profiles (i.e., gateway device profiles) are listed with a ?type=gateway query parameter.
Configurable Authentication

Reads a local file Token-Org.txt which contains:
makefile
Copy
token=<Your Mist API Token>
org_id=<Your Organization ID>
Ensures your API token and Org ID are not hardcoded in the script.
Failsafe Prompts

The script prompts for confirmation before deleting items—either one-by-one or for an entire set.
Modular Design

Each “section” of resources is defined in a sections dictionary for clarity and easy maintenance:
python
Copy
sections = {
  "1": {"name": "Sites", ...},
  "2": {"name": "Applications", ...},
  ...
}
Each section specifies the API endpoints for listing and deleting.
How It Works
Reading the Token & Org ID

At startup, the script calls read_token_org(), which looks for a file named Token-Org.txt.
It extracts two lines:
makefile
Copy
token=<your_mist_api_token>
org_id=<your_org_id>
If not found, the script exits and instructs you to create/update this file.
Sections and API Paths

There is a global sections dictionary that maps each resource “type” (e.g. Sites, Applications, etc.) to its list and delete paths.
List Path: Called with GET to retrieve all items from a resource.
Delete Path: Called with DELETE for a single item ID.
Listing Items

When you select a section from the menu, the script constructs the list_path (inserting org_id if needed) and calls the Mist API with GET.
It then displays each item with a name, ID, and its index in the list.
Deleting Items

After listing, the script prompts you to choose which items to delete. You can:
Enter individual numbers (e.g. 1,3,5) to selectively delete items
Type “all” to remove every item in that section
Type “exit” to go back without deleting
For each item you choose, the script calls the delete_path with a DELETE request.
Remove All

The menu also includes a “Remove All (All Sections)” option.
This triggers a single confirmation and then iterates through all sections, listing and deleting items in each one.
Error Handling

The script prints error messages if the request fails (e.g., HTTP 404 or 400).
Successfully deleted items typically return an HTTP 204 or 200.
Requirements
Python 3.x
requests library
You can install via:
bash
Copy
pip install requests
A valid Mist API token and Org ID.
Setup
Install Dependencies

bash
Copy
pip install requests
Create or Update Token-Org.txt
In the same folder as your script, create a file named Token-Org.txt with the following format:

makefile
Copy
token=YOUR_MIST_API_TOKEN
org_id=YOUR_ORGANIZATION_ID
Make sure it’s not tracked in version control if it contains sensitive info.

Run the Script

bash
Copy
python your_script_name.py
If Token-Org.txt is present and valid, you’ll see a menu prompting for which section you want to manage.
Usage
Once running, you’ll see a menu like:

markdown
Copy
Choose a section to manage:
 1. Sites
 2. Applications
 3. Networks
 4. Hub Profiles
 5. WAN Edges
 6. Remove All (All Sections)
 0. Exit
Enter a number (1-5) to manage that resource type.
The script will list all found items.
You can choose which IDs to delete individually, or type “all” to delete them all in that category.
Enter “6” to remove every resource (across all categories) at once.
You’ll get a final confirmation “Are you absolutely sure?”
Enter “0” to exit.
Example
Delete a Single Site

Choose 1 for Sites.
The script prints all existing sites, each with an index (1, 2, 3, …).
Enter the index (e.g. 2) to remove the second site.
Confirm with “yes” or skip with “no.”
Delete All Hub Profiles

Choose 4 for Hub Profiles.
Enter all at the prompt.
Confirm with “yes” to remove every hub profile returned by the listing.
Remove Everything

Choose 6.
If you confirm “yes,” the script iterates through all sections (Sites, Applications, Networks, Hub Profiles, and WAN Edges) and deletes every item found in each.
Contributing
If you have additional resources to manage or want to adjust the script for other endpoints, you can simply modify the sections dictionary in the code:

python
Copy
sections = {
   "1": {
       "name": "Sites",
       "list_path": "/orgs/{org_id}/sites",
       "delete_path": "/sites"
   },
   ...
}
list_path is where the GET request pulls item lists from.
delete_path is the base for DELETE calls (appending /{item_id}).
Insert "{org_id}" in the path if the endpoint requires the organization context.
That’s it! This script should simplify your organization’s cleanup tasks in Mist by exposing an interactive, confirm-driven interface for listing and deleting resources.
