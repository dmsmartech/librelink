[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/dmsmartech/librelink)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

# LibreLink Up — Home Assistant Integration

🇬🇧 English | [🇮🇹 Italiano](README_IT.md)

---

This integration allows you to display FreeStyle Libre glucose data in Home Assistant, read via the Abbott LibreLink Up app.

---

## How it works

The FreeStyle Libre sensor transmits data to the **LibreApp** (or **FreeStyle LibreLink**) app on the patient's phone. Via the sharing feature, this data is sent to the cloud and made available to a second account through the **LibreLink Up** app.

The Home Assistant integration connects to this second LibreLink Up account to read the data.

---

## Prerequisites

- An active FreeStyle Libre sensor
- The **LibreApp** (or FreeStyle LibreLink) app installed on the patient's phone, with a registered Abbott account
- A **second Abbott account** to use with LibreLink Up (can be a secondary account of yours)
- The **LibreLink Up** app installed on the patient's phone
- Home Assistant with HACS installed

---

## Step 1 — Invite the second account from LibreApp

On the patient's phone, in the **LibreApp** app:

1. Open the app and tap the menu icon in the top left
2. Select **Connected apps**
3. Tap **Connect** (if you haven't invited anyone yet) or **Manage** (if you've already invited someone)
4. Tap the **Add connection** button
5. Fill in the form with the required details
6. Send the invitation

---

## Step 2 — Accept the invitation in LibreLink Up

On the phone where you have **LibreLink Up** installed:

1. Open the LibreLink Up app
2. Log in with the second Abbott account (the one the invitation was sent to)
3. Accept the received invitation
4. **Accept Abbott's Terms of Service** — this step is mandatory: without it the integration will not work
5. Verify that the patient's glucose data is visible in the app

> **Important:** every time Abbott updates the Terms of Service, you will need to reopen the LibreLink Up app and accept them again before the integration will work. In some cases it may be necessary to log out of the LibreLink Up account and log back in to see the new Terms of Service.

---

## Step 3 — Install the integration in Home Assistant

### Via HACS

1. Open HACS in Home Assistant
2. Go to **Integrations** → click the three dots in the top right → **Custom repositories**
3. Enter the repository URL: `https://github.com/dmsmartech/librelink`
4. Select the category **Integration**
5. Click **Add**
6. Search for **LibreLink** in HACS and install it
7. Restart Home Assistant

---

## Step 4 — Configure the integration

1. In Home Assistant go to **Settings** → **Devices & services**
2. Click **Add integration** and search for **LibreLink**
3. Enter:
   - **Email** and **Password** of the second Abbott account (the LibreLink Up one)
   - **Region** — select the correct one for your country (e.g. Europe)
   - **Unit of measurement** — `mg/dL` or `mmol/L`
4. Click **Submit**

If the credentials are correct and the Terms of Service have been accepted in the app, the integration will connect and the sensors will be created automatically.

---

## Available sensors

For each patient linked to the LibreLink Up account, the following are created:

| Sensor | Description |
|---|---|
| Glucose measurement | Current value in mg/dL or mmol/L |
| Glucose trend | Text + icon (Stable, Increasing, Decreasing, etc.) |
| Active sensor (days) | Days since sensor activation |
| Minutes since last update | Minutes since the last sensor reading |
| Is high | Yes / No |
| Is low | Yes / No |

---

## Illustration with a custom:mini-graph-card

![image](https://github.com/gillesvs/librelink/assets/51242147/bfed1b2b-dbf7-4666-a202-885ff3db67b8)

And the yaml if you like this card:
https://github.com/gillesvs/librelink/blob/main/custom_components/librelink/mini-graph-glucose.yml

---

## Re-authentication

If the Terms of Service are updated and the integration stops working:

1. Open the LibreLink Up app and accept the new Terms of Service
2. In Home Assistant go to **Settings** → **Devices & services**
3. You will see a notification on the LibreLink integration — click **Re-authenticate**
4. Re-enter your credentials

There is no need to remove and reinstall the integration.

---

## Common issues

| Issue | Solution |
|---|---|
| Authentication error | Check the email and password of the second Abbott account |
| Terms of Service not accepted | Open LibreLink Up and accept the T&S, then re-authenticate |
| No data visible | Check that the invitation has been accepted and data is visible in LibreLink Up |
| Wrong region | Remove and reinstall the integration selecting the correct region |

---

## What's new in this fork

### v1.2.5 — LibreLink Up v5.0 compatibility
- **Fix: `Account-Id` header** — Abbott API now requires a SHA256-hashed account ID in every authenticated request. Without it, the API returns HTTP 400 `RequiredHeaderMissing`.
- **Fix: API version header** — updated from `4.7` to `4.16.0` (minimum required by Abbott since app v5.0).
- **Fix: HTTP 430 handling** — explicit error message when Terms of Service have not been accepted in the app.
- **New: Re-authentication flow** — Home Assistant now shows a re-authentication prompt directly in the UI when credentials expire or Terms of Service are updated.

---

## Credits

Based on the original work by [gillesvs/librelink](https://github.com/gillesvs/librelink).
