import openai
import os
import sys
import time
import threading
import json
import requests
from config import API_KEY, BASE_URL, MODEL_NAME

def show_loading_animation():
    animation = ["Processing.", "Processing..", "Processing..."]
    i = 0
    while loading[0]:
        sys.stdout.write('\r' + animation[i % len(animation)])
        sys.stdout.flush()
        time.sleep(0.5)
        i += 1
    sys.stdout.write('\r')
    sys.stdout.flush()

def process_text(text):
    try:
        # Initialize the client with custom base URL
        client = openai.OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )
        
        # Start loading animation
        global loading
        loading = [True]
        loading_thread = threading.Thread(target=show_loading_animation)
        loading_thread.start()
        
        # Define system prompt
        system_prompt = '''Your are a helpful, cheerful database assistant. 
Use the following database schema when creating your answers:
[{
    "table_name": "campaign_site_ad_for_ecpm_update",
    "fields": [
        {"name": "ga_campaign_id", "display_name": "Ga Campaign ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "pm_ad_id", "display_name": "Pm Ad ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "pm_site_id", "display_name": "Pm Site ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "pub_id", "display_name": "Pub ID", "description": null, "effective_type": "type/BigInteger"}
    ]
},{
    "table_name": "wrapper_abtest_groupsize",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/Integer"},
        {"name": "name", "display_name": "Name", "description": null, "effective_type": "type/Text"},
        {"name": "description", "display_name": "Description", "description": null, "effective_type": "type/Text"},
        {"name": "display_name", "display_name": "Display Name", "description": null, "effective_type": "type/Text"}
    ]
},{
    "table_name": "wrapper_abtest_type",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/Integer"},
        {"name": "name", "display_name": "Name", "description": null, "effective_type": "type/Text"},
        {"name": "description", "display_name": "Description", "description": null, "effective_type": "type/Text"},
        {"name": "display_name", "display_name": "Display Name", "description": null, "effective_type": "type/Text"}
    ]
},{
    "table_name": "wrapper_ad_integration_type",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/Integer"},
        {"name": "platform_id", "display_name": "Platform ID", "description": null, "effective_type": "type/Integer"},
        {"name": "integration_type", "display_name": "Integration Type", "description": null, "effective_type": "type/Text"},
        {"name": "method", "display_name": "Method", "description": null, "effective_type": "type/Text"},
        {"name": "endpoint", "display_name": "Endpoint", "description": null, "effective_type": "type/Text"},
        {"name": "endpoint_name", "display_name": "Endpoint Name", "description": null, "effective_type": "type/Text"},
        {"name": "creation_time", "display_name": "Creation Time", "description": null, "effective_type": "type/DateTimeWithLocalTZ"},
        {"name": "last_modified", "display_name": "Last Modified", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}
    ]
},{
    "table_name": "wrapper_ad_parameter_dependency_map",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/Integer"},
        {"name": "parent_object_group", "display_name": "Parent Object Group", "description": null, "effective_type": "type/Integer"},
        {"name": "child_object_group", "display_name": "Child Object Group", "description": null, "effective_type": "type/Integer"}
    ]
},{
    "table_name": "wrapper_ad_parameter_group",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/Integer"},
        {"name": "name", "display_name": "Name", "description": null, "effective_type": "type/Text"}
    ]
},{
    "table_name": "wrapper_ad_parameter_tag_type_mapping",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "parameter_id", "display_name": "Parameter ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "tag_type_id", "display_name": "Tag Type ID", "description": null, "effective_type": "type/Integer"}
    ]
},{
    "table_name": "wrapper_ad_pod",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "version_id", "display_name": "Version ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "pod_type", "display_name": "Pod Type", "description": null, "effective_type": "type/Text"},
        {"name": "ad_slots_config", "display_name": "Ad Slots Config", "description": null, "effective_type": "type/Text"},
        {"name": "s2s_ad_slots_config", "display_name": "S2s Ad Slots Config", "description": null, "effective_type": "type/Text"},
        {"name": "targeting", "display_name": "Targeting", "description": null, "effective_type": "type/Text"},
        {"name": "creation_time", "display_name": "Creation Time", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}
    ]
},{
    "table_name": "wrapper_ad_unit_config",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "profile_id", "display_name": "Profile ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "ad_unit_id", "display_name": "Ad Unit ID", "description": null, "effective_type": "type/BigInteger"},
        {"name": "config_id", "display_name": "Config ID", "description": null, "effective_type": "type/Integer"},
        {"name": "value", "display_name": "Value", "description": null, "effective_type": "type/Text"}
    ]
},{
    "table_name": "wrapper_ad_unit_format",
    "fields": [
        {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/Integer"},
        {"name": "name", "display_name": "Name", "description": null, "effective_type": "type/Text"},
        {"name": "description", "display_name": "Description", "description": null, "effective_type": "type/Text"},
        {"name": "display_name", "display_name": "Display Name", "description": null, "effective_type": "type/Text"}
    ]
},{
    "table_name": "wrapper_global_code_version",
    "fields": [ { "name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger" }, { "name": "is_live", "display_name": "Is Live", "description": null, "effective_type": "type/Integer" }, { "name": "prebid_base_version", "display_name": "Prebid Base Version", "description": null, "effective_type": "type/Text" }, { "name": "release_date", "display_name": "Release Date", "description": null, "effective_type": "type/DateTimeWithLocalTZ" }, { "name": "release_name", "display_name": "Release Name", "description": null, "effective_type": "type/Text" }, { "name": "release_notes_url", "display_name": "Release Notes URL", "description": null, "effective_type": "type/Text" }, { "name": "release_summary", "display_name": "Release Summary", "description": "details about this release", "effective_type": "type/Text" }, { "name": "release_type_id", "display_name": "Release Type ID", "description": null, "effective_type": "type/Integer" }, { "name": "snapshot_json", "display_name": "Snapshot Json", "description": null, "effective_type": "type/Text" }, { "name": "is_disabled", "display_name": "Is Disabled", "description": "This column is used for disabling OpenWrap release versions", "effective_type": "type/Integer" }]
},{
    "table_name": "wrapper_live_code",
    "fields": [ { "name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger" }, { "name": "status", "display_name": "Status", "description": null, "effective_type": "type/Text" }, { "name": "created_at", "display_name": "Created At", "description": null, "effective_type": "type/DateTimeWithLocalTZ" }, { "name": "updated_at", "display_name": "Updated At", "description": null, "effective_type": "type/DateTimeWithLocalTZ" }, { "name": "version", "display_name": "Version", "description": "Version of the live code", "effective_type": "type/Text" }, { "name": "author", "display_name": "Author", "description": "The author of the live code", "effective_type": "type/Text" }, { "name": "is_active", "display_name": "Is Active", "description": "Indicates if the code version is currently active", "effective_type": "type/Boolean" } ]
},{
    "table_name": "wrapper_status",
    "fields": [ { "name": "cdn_refresh_id", "display_name": "Cdn Refresh ID", "description": null, "effective_type": "type/BigInteger" }, { "name": "modification_time", "display_name": "Modification Time", "description": null, "effective_type": "type/DateTimeWithLocalTZ" }, { "name": "status", "display_name": "Status", "description": "this shows status of wrapper, it could be live or staging or draft", "effective_type": "type/*" }, { "name": "version_id", "display_name": "Version ID", "description": null, "effective_type": "type/BigInteger" } ]
},{
    "table_name": "wrapper_profile",
    "fields": [{"name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "is_disabled", "display_name": "Is Disabled", "description": null, "effective_type": "type/Integer"}, {"name": "name", "display_name": "Name", "description": null, "effective_type": "type/Text"}, {"name": "pub_id", "display_name": "Pub ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "type", "display_name": "Type", "description": "1 means OpenWrap and 2 means IDhub or identity hub", "effective_type": "type/Boolean"}, {"name": "api_version", "display_name": "Api Version", "description": null, "effective_type": "type/Integer"}, {"name": "platform", "display_name": "Platform", "description": null, "effective_type": "type/Text"}, {"name": "is_action_required", "display_name": "Is Action Required", "description": null, "effective_type": "type/Integer"}]
},{
    "table_name": "wrapper_version",
    "fields": [{"name": "comment", "display_name": "Comment", "description": null, "effective_type": "type/Text"}, {"name": "creation_time", "display_name": "Creation Time", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}, {"name": "display_version", "display_name": "Display Version", "description": null, "effective_type": "type/BigInteger"}, {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "last_modified", "display_name": "Last Modified", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}, {"name": "profile_id", "display_name": "Profile ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "script_size", "display_name": "Script Size", "description": null, "effective_type": "type/Float"}]
},{
    "table_name": "wrapper_version_to_code_map",
    "fields": [{"name": "code", "display_name": "Code", "description": null, "effective_type": "type/Text"}, {"name": "global_code_version_id", "display_name": "Global Code Version ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "last_modified", "display_name": "Last Modified", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}, {"name": "version_id", "display_name": "Version ID", "description": null, "effective_type": "type/BigInteger"}]
},{
    "table_name": "wrapper_config_map",
    "fields": [{"name": "config_id", "display_name": "Config ID", "description": null, "effective_type": "type/Integer"}, {"name": "creation_time", "display_name": "Creation Time", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}, {"name": "entity_id", "display_name": "Entity ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "entity_type_id", "display_name": "Entity Type ID", "description": null, "effective_type": "type/Integer"}, {"name": "id", "display_name": "ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "is_active", "display_name": "Is Active", "description": null, "effective_type": "type/Boolean"}, {"name": "modification_time", "display_name": "Modification Time", "description": null, "effective_type": "type/DateTimeWithLocalTZ"}, {"name": "partner_id", "display_name": "Partner ID", "description": null, "effective_type": "type/BigInteger"}, {"name": "value", "display_name": "Value", "description": null, "effective_type": "type/Text"}, {"name": "test_config", "display_name": "Test Config", "description": null, "effective_type": "type/Boolean"}]
}]

Include column name headers in the query results.

Always provide your answer in the JSON format below:

{ "summary": "your-summary", "query":  "your-query" }

Output ONLY JSON.
In the preceding JSON response, substitute "your-query" with Microsoft SQL Server Query to retrieve the requested data.
In the preceding JSON response, substitute "your-summary" with a summary of the query.
Always include all columns in the table.
If the resulting query is non-executable, replace "your-query" with NA, but still substitute "your-query" with a summary of the query.
Do not use MySQL syntax. 
Do not add "\n" to the query only add a space
Always limit the SQL Query to 100 rows.'''
        
        # Make API request
        prompt = f"Generate a SQL query for the following request:\n\n{text}"
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Stop loading animation
        loading[0] = False
        loading_thread.join()
        
        result = response.choices[0].message.content.strip()
        query = None
        
        try:
            # Print raw response for debugging
            print("\nRaw API response:")
            print(result)
            
            # Parse the JSON result
            json_result = json.loads(result)
            # Extract and print only the query property
            query = json_result.get("query", "No query found in response")
            print("\n✅ SQL Query generated successfully!")
            print("\nQuery:", query)
        except json.JSONDecodeError as e:
            print(f"\n⚠️ Could not parse JSON response. Error: {str(e)}")
            print("Raw result:", result)
            
            # Try to extract query with a fallback approach
            if "query" in result:
                try:
                    # Try to find the query part using string manipulation
                    start_idx = result.find('"query":') + 9  # Length of '"query": "'
                    if start_idx > 9:  # Found "query":
                        # Find the closing quote, accounting for escaped quotes
                        end_idx = start_idx
                        in_escape = False
                        for i in range(start_idx, len(result)):
                            if result[i] == '\\':
                                in_escape = not in_escape
                                continue
                            if result[i] == '"' and not in_escape:
                                end_idx = i
                                break
                            in_escape = False
                        
                        if end_idx > start_idx:
                            query = result[start_idx:end_idx]
                            print("\n✅ Extracted query using fallback method:")
                            print("\nQuery:", query)
                except Exception as ex:
                    print(f"Fallback extraction failed: {str(ex)}")
            
            if not query:
                return False
        
        # Make a POST request to the dataset API
        if query and query != "No query found in response":
            try:
                print("\nSending query to dataset API...")
                payload = {
                    "type": "native",
                    "native": {
                        "query": query,
                        "template-tags": {}
                    },
                    "database": 7,
                    "parameters": []
                }
                
                response = requests.post(
                    "https://braavos.pubmatic.com/api/dataset",
                    json=payload
                )
                
                if response.status_code == 200:
                    print("✅ Query successfully sent to dataset API!")
                    try:
                        if response.text.strip():  # Check if response is not empty
                            response_json = response.json()
                            print("Response:", response_json)
                        else:
                            print("Response: [Empty response]")
                    except json.JSONDecodeError:
                        print("Response: [Non-JSON response]")
                        print("Raw response text:", response.text)
                else:
                    print(f"❌ Dataset API request failed with status code: {response.status_code}")
                    print("Response:", response.text)
            except Exception as e:
                print(f"❌ Error sending query to dataset API: {str(e)}")
        
        return True
        
    except Exception as e:
        # Stop loading animation in case of error
        loading[0] = False
        loading_thread.join()
        
        print("\n❌ API request failed!")
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    user_text = input("Enter your SQL query request: ")
    if user_text.strip():
        process_text(user_text.strip())
    else:
        print("No text provided. Exiting.")