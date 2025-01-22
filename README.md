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
