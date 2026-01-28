#!/usr/bin/env python3
"""
Hush K8s Goat App - Authentication Event Generator

Generates authentication events by calling the HubSpot API in a loop.
Used to demonstrate and validate Hush NHI tracking capabilities.
"""

import os
import sys
import time
import logging
import requests

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Configuration from environment
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", "")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "30"))
HUBSPOT_API_URL = "https://api.hubapi.com/crm/v3/objects/contacts"


def check_hubspot_auth() -> dict:
    """
    Attempt to authenticate with HubSpot API.
    Returns dict with success status and details.
    """
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(HUBSPOT_API_URL, headers=headers, timeout=10)
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "message": "Authentication successful" if response.status_code == 200 else response.text[:200],
        }
    except requests.exceptions.Timeout:
        return {"success": False, "status_code": 0, "message": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "status_code": 0, "message": str(e)[:200]}


def main():
    """Main loop - authenticate to HubSpot API at regular intervals."""
    logger.info("=" * 50)
    logger.info("Hush K8s Goat App - Starting")
    logger.info("=" * 50)
    logger.info(f"Target: HubSpot API ({HUBSPOT_API_URL})")
    logger.info(f"Interval: {INTERVAL_SECONDS} seconds")
    logger.info(f"API Key: {'*' * 8}...{HUBSPOT_API_KEY[-4:] if len(HUBSPOT_API_KEY) > 4 else '(not set)'}")
    logger.info("=" * 50)

    if not HUBSPOT_API_KEY:
        logger.warning("HUBSPOT_API_KEY not set - will generate failed auth events")

    attempt = 0
    while True:
        attempt += 1
        logger.info(f"[Attempt #{attempt}] Authenticating to HubSpot API...")

        result = check_hubspot_auth()

        if result["success"]:
            logger.info(f"[Attempt #{attempt}] SUCCESS - Status: {result['status_code']}")
        else:
            logger.warning(
                f"[Attempt #{attempt}] FAILED - Status: {result['status_code']} - {result['message']}"
            )

        logger.info(f"Sleeping for {INTERVAL_SECONDS} seconds...")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
