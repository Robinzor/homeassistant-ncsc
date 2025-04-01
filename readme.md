# Home Assistant NCSC Advisories Sensor

This custom component for Home Assistant fetches the latest security advisories from the Dutch National Cyber Security Centre (NCSC) using their RSS feed.

## Features
- Retrieves and displays the latest advisories from [NCSC RSS Feed](https://advisories.ncsc.nl/rss/advisories)
- Updates every minute to ensure the latest information is available
- Stores the last 10 advisories as state attributes
- Supports Home Assistant notifications when a new advisory is detected

## Installation

1. **Download the files**
   - Copy the `ncsc` folder into your Home Assistant `custom_components` directory.
   
     The structure should look like this:
     ```
     config/
     ├── custom_components/
     │   ├── ncsc/
     │   │   ├── __init__.py
     │   │   ├── sensor.py
     │   │   ├── manifest.json
     ```

2. **Restart Home Assistant**
   - After adding the files, restart Home Assistant to load the custom component.

3. **Add to `configuration.yaml`**
   - Include the sensor configuration:
     ```yaml
     sensor:
       - platform: ncsc
     ```

4. **Reload Home Assistant**
   - Navigate to Developer Tools -> Check Configuration -> Restart Home Assistant.

## Automation: Send Notification on New Advisory

You can set up an automation in Home Assistant to send a notification when a new advisory is published.

### Example Automation:
```yaml
alias: "NCSC Advisory Notification"
description: "Send a mobile notification when a new NCSC advisory is detected."
trigger:
  - platform: state
    entity_id: sensor.ncsc_advisories
    to: "!None"
action:
  - service: notify.mobile_app_YOUR_DEVICE_NAME
    data:
      title: "New NCSC Advisory Alert!"
      message: "{{ states('sensor.ncsc_advisories') }}"
mode: single
