#!/usr/bin/env python3
"""
Apply corrections to Make.com scenario 4885612 (ALTAVIDA Meta Ads → Kommo).

Fixes applied:
  - Module 3 (WhatsApp 360dialog): "521{{telefono}}" → "52{{telefono}}"
  - Module 7 (Kommo POST /leads): PHONE+EMAIL moved into _embedded.contacts

Usage:
  export MAKE_API_KEY="your-key-from-make-com-profile"
  python3 apply-make-fix.py

Get your API key at: https://us2.make.com/user/api
"""

import json
import os
import sys
import urllib.request
import urllib.error

MAKE_BASE_URL = "https://us2.make.com"
SCENARIO_ID = 4885612
TEAM_ID = 2213687

def make_api_request(method, path, body=None):
    api_key = os.environ.get("MAKE_API_KEY")
    if not api_key:
        print("ERROR: Set MAKE_API_KEY environment variable first.")
        print("Get it at: https://us2.make.com/user/api")
        sys.exit(1)

    url = f"{MAKE_BASE_URL}{path}"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"HTTP {e.code} {e.reason}: {err_body}")
        sys.exit(1)


def main():
    print(f"Fetching scenario {SCENARIO_ID}...")
    resp = make_api_request("GET", f"/api/v2/scenarios/{SCENARIO_ID}")
    scenario = resp.get("scenario") or resp
    blueprint = scenario["blueprint"]

    print("Applying fixes...")
    fixed = 0
    for module in blueprint["flow"]:
        mid = module["id"]
        mapper = module.get("mapper", {})

        if mid == 3:
            body_str = mapper.get("jsonStringBodyContent", "")
            if "521{{1.telefono}}" in body_str:
                mapper["jsonStringBodyContent"] = body_str.replace(
                    "521{{1.telefono}}", "52{{1.telefono}}"
                )
                print("  [OK] Module 3: fixed phone prefix 521 → 52")
                fixed += 1
            else:
                print("  [SKIP] Module 3: phone prefix already correct or format differs")

        if mid == 7:
            body_str = mapper.get("jsonStringBodyContent", "")
            try:
                body = json.loads(body_str)
                lead = body[0]
                # Check if it still uses the wrong flat structure
                if "custom_fields_values" in lead and "_embedded" not in lead:
                    corrected_body = [
                        {
                            "name": lead["name"],
                            "_embedded": {
                                "contacts": [
                                    {
                                        "name": "{{1.nombre}}",
                                        "custom_fields_values": [
                                            {
                                                "field_code": "PHONE",
                                                "values": [{"value": "{{1.telefono}}", "enum_code": "MOB"}]
                                            },
                                            {
                                                "field_code": "EMAIL",
                                                "values": [{"value": "{{1.email}}", "enum_code": "WORK"}]
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                    mapper["jsonStringBodyContent"] = json.dumps(corrected_body, separators=(",", ":"))
                    print("  [OK] Module 7: moved PHONE+EMAIL into _embedded.contacts")
                    fixed += 1
                elif "_embedded" in lead:
                    print("  [SKIP] Module 7: _embedded.contacts already present")
                else:
                    print(f"  [WARN] Module 7: unexpected body structure — manual check needed")
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                print(f"  [ERROR] Module 7: could not parse body — {e}")

    if fixed == 0:
        print("No changes needed — scenario already correct.")
        return

    print(f"\nApplying {fixed} fix(es) to scenario {SCENARIO_ID}...")
    update_resp = make_api_request(
        "PATCH",
        f"/api/v2/scenarios/{SCENARIO_ID}",
        {"blueprint": blueprint}
    )
    print("Scenario updated successfully.")
    print(f"Last edit: {update_resp.get('scenario', update_resp).get('lastEdit', 'n/a')}")

    print("\nSending test lead to webhook...")
    test_payload = {
        "nombre": "Test Claude Code",
        "telefono": "9984894142",
        "email": "test@altavida.mx",
        "canal": "Meta Ads",
        "propiedad": "Aqua Residencial"
    }
    webhook_url = "https://hook.us2.make.com/tmn161mw17n3ipiwp28irr0pgebvf3gf"
    wh_req = urllib.request.Request(
        webhook_url,
        data=json.dumps(test_payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(wh_req) as wh_resp:
            print(f"Webhook response: {wh_resp.status} {wh_resp.read().decode()}")
    except urllib.error.HTTPError as e:
        print(f"Webhook HTTP {e.code}: {e.read().decode()}")

    print("\nDone. Check davissmarin.kommo.com/leads for the test lead.")


if __name__ == "__main__":
    main()
