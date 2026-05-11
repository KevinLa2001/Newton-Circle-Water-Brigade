\# Newton Circle Water Brigade



The \*\*Newton Circle Water Brigade\*\* app coordinates community watering responsibilities for the Newton Circle neighborhood. It automates scheduling, weather‑based adjustments, notifications, and volunteer sign‑ups. The app ensures watering is covered on designated days, avoids unnecessary watering during rain, and adds extra watering days during heat events.



\---



\## Features



\### ✔️ Watering Schedule (M/W/F/S/S)

The base watering pattern includes:

\- Monday

\- Wednesday

\- Friday

\- Saturday

\- Sunday



No watering on:

\- Tuesday

\- Thursday



\### ✔️ Rain‑Day Automation

If the chance of rain is \*\*≥ 80%\*\* (admin adjustable):

\- The day is marked as \*\*Rain\*\*

\- Optional: volunteer assignment is cleared

\- Users are notified: \*“Rain expected today. No watering needed.”\*

\- Nagging reminders are suppressed

\- Heat‑triggered days are not created



\### ✔️ Heat‑Triggered Watering Days

If the forecasted high temperature is \*\*≥ 80°F\*\*:

\- Extra watering days are added (including Tue/Thu)

\- These are marked as \*\*Heat‑Triggered\*\*

\- Users are notified

\- Nagging continues until filled



\### ✔️ Volunteer Sign‑Up \& Removal

\- Users can sign up for any open watering day

\- Users can remove themselves from a day they previously claimed

\- Removing yourself triggers a group notification



\### ✔️ Daily Nagging System

At \*\*8 AM\*\*, the system notifies all users of any \*\*Open\*\* slots.

Nagging is skipped for:

\- Rain days

\- Filled days

\- Past days



\### ✔️ Notifications

Users receive:

\- Open slot alerts

\- Rain‑day alerts

\- Heat‑triggered day alerts

\- Sign‑up confirmations

\- Removal confirmations



\---



\## User Roles



\### Regular Users

\- View the calendar

\- Sign up for watering days

\- Remove themselves

\- Receive notifications



\### Admins

Admins can:

\- Adjust rain threshold

\- Adjust heat threshold

\- Toggle auto‑clear on rain days

\- Set season start/end

\- Manage users

\- Override assignments

\- View activity logs



\---



\## Data Model



\### WateringSlot

| Field | Type | Description |

|-------|------|-------------|

| id | GUID | Unique slot ID |

| date | Date | Watering date |

| assignedTo | String | User name or empty |

| status | Enum | Open, Filled, Rain, Past |

| isHeatTriggered | Boolean | True if created by heat rule |

| isRainDay | Boolean | True if rain threshold met |

| rainProbability | Number | % chance of rain |

| notificationsSent | Boolean | Tracks vacancy alerts |



\### User

| Field | Type | Description |

|-------|------|-------------|

| id | GUID | Unique user ID |

| name | String | Display name |

| contact | String | Email or phone |

| isAdmin | Boolean | Admin privileges |



\### Admin Settings

| Field | Type | Description |

|-------|------|-------------|

| rainThreshold | Number | Default 80% |

| heatThreshold | Number | Default 80°F |

| autoClearOnRain | Boolean | Default true |

| seasonStart | Date | Season start |

| seasonEnd | Date | Season end |

| wateringPattern | Array | \[Mon, Wed, Fri, Sat, Sun] |



\---



\## Automation Logic



\### Schedule Generator

\- Generates slots only on M/W/F/S/S

\- Default values:

&#x20; - status = Open

&#x20; - isRainDay = false

&#x20; - isHeatTriggered = false



\### Rain Rule (6 AM)

1\. Fetch rain probability

2\. If ≥ threshold:

&#x20;  - Mark slot as Rain

&#x20;  - Clear volunteer (if enabled)

&#x20;  - Notify users

&#x20;  - Suppress nagging



\### Heat Rule (6 AM)

1\. Fetch high temperature

2\. If ≥ threshold AND not a rain day:

&#x20;  - Add heat‑triggered slots

&#x20;  - Notify users

&#x20;  - Nag until filled



\### Vacancy Detection

Triggered when a user removes themselves:

\- Notify group that the slot is open



\### Daily Nagging (8 AM)

\- Notify users of all \*\*Open\*\* slots

\- Skip if:

&#x20; - Rain

&#x20; - Filled

&#x20; - Past



\---



\## UI Structure



\### Screens

1\. \*\*Home / Calendar\*\*

2\. \*\*Day Detail\*\*

3\. \*\*Sign‑Up Modal\*\*

4\. \*\*Remove Modal\*\*

5\. \*\*Notifications Center\*\*

6\. \*\*Settings (Admin)\*\*

7\. \*\*Subscreens\*\*

&#x20;  - Season settings

&#x20;  - Weather automation

&#x20;  - User management

&#x20;  - Activity log



\### Calendar Color Coding

\- \*\*Green\*\* = Filled

\- \*\*Red\*\* = Open

\- \*\*Blue\*\* = Rain

\- \*\*Yellow\*\* = Heat‑Triggered

\- \*\*Gray\*\* = No watering day



\---



\## Technology Recommendations

This app is optimized for:

\- \*\*Power Apps (Canvas App)\*\*

\- \*\*Power Automate\*\* for weather checks, nagging, and automation

\- \*\*Microsoft Lists or Dataverse\*\* for data storage



\---



\## Status

\*\*Specification: Finalized\*\*

Ready for implementation.

# Newton-Circle-Water-Brigade
