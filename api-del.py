import requests

def read_token_org(file_path="Token-Org.txt"):
    """Reads the token and org_id from the specified file."""
    try:
        with open(file_path, 'r') as f:
            token, org_id = None, None
            for line in f:
                if line.startswith("token="):
                    token = line.split("=", 1)[1].strip()
                elif line.startswith("org_id="):
                    org_id = line.split("=", 1)[1].strip()
            if not token or not org_id:
                raise ValueError("Token or Org ID not found.")
            return token, org_id
    except FileNotFoundError:
        print("[ERROR] Token-Org.txt file not found. Please ensure it exists with 'token=<your_token>' and 'org_id=<your_org_id>'.")
        exit(1)

#
# We define each section with:
#   "name": Display label
#   "list_path": path (after /api/v1) used for listing items
#   "delete_path": path (after /api/v1) used for deleting a single item
#
#   NOTE: The {org_id} placeholder must be included if needed.
#         For Sites, listing is /orgs/{org_id}/sites but deletion is /sites/:site_id
#         For Hub (Gateway) Profiles, we add ?type=gateway to filter for those.
#
sections = {
    "1": {
        "name": "Sites",
        # GET /api/v1/orgs/{org_id}/sites
        "list_path": "/orgs/{org_id}/sites",
        # DELETE /api/v1/sites/{site_id}
        "delete_path": "/sites"
    },
    "2": {
        "name": "Applications",
        # GET /api/v1/orgs/{org_id}/services
        "list_path": "/orgs/{org_id}/services",
        # DELETE /api/v1/orgs/{org_id}/services/:service_id
        "delete_path": "/orgs/{org_id}/services"
    },
    "3": {
        "name": "Networks",
        # GET /api/v1/orgs/{org_id}/networks
        "list_path": "/orgs/{org_id}/networks",
        # DELETE /api/v1/orgs/{org_id}/networks/:network_id
        "delete_path": "/orgs/{org_id}/networks"
    },
    "4": {
        "name": "Hub Profiles",
        # GET /api/v1/orgs/{org_id}/deviceprofiles?type=gateway  <-- specifically for gateway (hub) type
        "list_path": "/orgs/{org_id}/deviceprofiles?type=gateway",
        # DELETE /api/v1/orgs/{org_id}/deviceprofiles/:profile_id
        "delete_path": "/orgs/{org_id}/deviceprofiles"
    },
    "5": {
        "name": "WAN Edges",
        # GET /api/v1/orgs/{org_id}/gatewaytemplates
        "list_path": "/orgs/{org_id}/gatewaytemplates",
        # DELETE /api/v1/orgs/{org_id}/gatewaytemplates/:template_id
        "delete_path": "/orgs/{org_id}/gatewaytemplates"
    }
}

def list_items(token, org_id, section, list_path):
    """
    Lists all items for the specified section from /api/v1{list_path}.
    Example: /api/v1/orgs/{org_id}/sites
    """
    base_url = "https://api.mist.com/api/v1"
    # Insert org_id into the list_path if {org_id} is present
    url = base_url + list_path.format(org_id=org_id)

    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        items = response.json()
        if not items:
            print(f"[INFO] No {section} found.")
            return []
        print(f"[INFO] Retrieved {section}:")
        for i, item in enumerate(items, start=1):
            print(f" {i}. {item.get('name', 'Unnamed')} (ID: {item['id']})")
        return items
    else:
        print(f"[ERROR] Failed to retrieve {section}. Status: {response.status_code}")
        print(f"[ERROR] Response: {response.text}")
        return []

def delete_item(token, org_id, delete_path, item_id):
    """
    Deletes an item by ID using /api/v1{delete_path}/{item_id}.
    Example: /api/v1/sites/{site_id} or /api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}
    """
    base_url = "https://api.mist.com/api/v1"

    # Insert org_id into the delete_path if it has {org_id} placeholder
    path = delete_path.format(org_id=org_id)

    # Build full URL for the individual item
    url = f"{base_url}{path}/{item_id}"
    headers = {"Authorization": f"Token {token}"}
    response = requests.delete(url, headers=headers)

    if response.status_code in [200, 204]:
        print(f"[INFO] Successfully deleted item with ID: {item_id}")
    elif response.status_code == 404:
        print(f"[ERROR] Item with ID {item_id} not found or already deleted.")
    else:
        print(f"[ERROR] Failed to delete item with ID {item_id}. Status: {response.status_code}")
        print(f"[ERROR] Response: {response.text}")


def remove_all_in_section(token, org_id, section_choice):
    """
    Lists all items in a single section and deletes them all (with confirmation).
    """
    section_name = sections[section_choice]["name"]
    list_path    = sections[section_choice]["list_path"]
    delete_path  = sections[section_choice]["delete_path"]

    items = list_items(token, org_id, section_name, list_path)
    if not items:
        return  # No items, nothing to delete

    for item in items:
        delete_item(token, org_id, delete_path, item['id'])


def main():
    token, org_id = read_token_org()
    print("[INFO] Token and Org ID loaded successfully.")

    while True:
        print("\nChoose a section to manage:")
        for key in sorted(sections.keys()):
            print(f" {key}. {sections[key]['name']}")
        print(" 6. Remove All (All Sections)")
        print(" 0. Exit")

        section_choice = input("Enter your choice: ").strip()
        if section_choice == "0":
            print("[INFO] Exiting.")
            break
        elif section_choice == "6":
            # Remove everything from all sections in one pass
            print("You chose to delete EVERYTHING from all sections (1-5).")
            confirm = input("Are you absolutely sure? (yes/no): ").strip().lower()
            if confirm == "yes":
                for s_key in sorted(sections.keys()):
                    remove_all_in_section(token, org_id, s_key)
                print("[INFO] All sections cleared (where items existed).")
            else:
                print("[INFO] Aborted 'Remove All'.")
        elif section_choice in sections:
            # Normal per-section logic
            section_name   = sections[section_choice]["name"]
            list_path      = sections[section_choice]["list_path"]
            delete_path    = sections[section_choice]["delete_path"]

            items = list_items(token, org_id, section_name, list_path)
            if not items:
                continue

            print(f"\nEnter the numbers of the {section_name.lower()} to delete, separated by commas (e.g., 1,3,5),")
            print(" or type 'all' to delete ALL from this section, or 'exit' to return.")
            user_input = input("Your choice: ").strip().lower()

            if user_input == "exit":
                print(f"[INFO] Returning to main menu.")
                continue
            elif user_input == "all":
                confirmation = input(f"Are you sure you want to delete ALL {section_name.lower()}? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    for item in items:
                        delete_item(token, org_id, delete_path, item['id'])
                else:
                    print(f"[INFO] Deletion canceled.")
            else:
                try:
                    selections = [int(num.strip()) for num in user_input.split(",") if num.strip().isdigit()]
                    for index in selections:
                        if 1 <= index <= len(items):
                            item = items[index - 1]
                            confirmation = input(
                                f"Are you sure you want to delete {section_name.lower()} "
                                f"'{item.get('name', 'Unnamed')}' (ID: {item['id']})? (yes/no): "
                            ).strip().lower()
                            if confirmation == "yes":
                                delete_item(token, org_id, delete_path, item['id'])
                            else:
                                print(f"[INFO] Skipping deletion of {section_name.lower()} '{item.get('name', 'Unnamed')}'.")
                        else:
                            print(f"[ERROR] Invalid {section_name.lower()} number: {index}")
                except ValueError:
                    print(f"[ERROR] Invalid input. Please enter numbers separated by commas or 'all'.")

            # Show remaining items after deletions
            print(f"\n[INFO] Remaining {section_name}:")
            list_items(token, org_id, section_name, list_path)
        else:
            print("[ERROR] Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
