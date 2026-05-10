\# Newton Circle Water Brigade — Final Specification



\## Overview

The \*\*Newton Circle Water Brigade\*\* app coordinates community watering responsibilities for the Newton Circle neighborhood. It automates scheduling, weather‑based adjustments, notifications, and volunteer sign‑ups. The system ensures watering is covered on designated days, avoids unnecessary watering during rain, and adds extra watering days during heat events.



This document defines the complete functional specification for the app.



\---



\# 1. Watering Schedule Rules



\## 1.1 Base Watering Pattern

Watering occurs on:

\- Monday  

\- Wednesday  

\- Friday  

\- Saturday  

\- Sunday  



No watering on:

\- Tuesday  

\- Thursday  



\## 1.2 Heat‑Triggered Days

If the forecasted high temperature is \*\*≥ 80°F\*\*:

\- Add watering slots on any sunny day (including Tue/Thu)

\- Mark these as \*\*Heat‑Triggered\*\*

\- Notify all users

\- Nag until filled



\## 1.3 Rain‑Day Logic

If the chance of rain is \*\*≥ 80%\*\* (admin adjustable):

\- Mark the day as \*\*Rain\*\*

\- Optional: clear volunteer assignment (admin toggle)

\- Notify users: \*“Rain expected today. No watering needed.”\*

\- Suppress nagging

\- Do not create heat‑triggered days on rain days



\---



\# 2. User Roles



\## 2.1 Regular Users

\- View the calendar  

\- Sign up for watering days  

\- Remove themselves  

\- Receive notifications  



\## 2.2 Admins

Admins can:

\- Adjust rain threshold  

\- Adjust heat threshold  

\- Toggle auto‑clear on rain days  

\- Set season start/end  

\- Manage users  

\- Override assignments  

\- View activity logs  



\---



\# 3. Features



\## 3.1 Calendar View

\- Monthly calendar  

\- Color‑coded days:

&#x20; - \*\*Green\*\* = Filled  

&#x20; - \*\*Red\*\* = Open  

&#x20; - \*\*Blue\*\* = Rain  

&#x20; - \*\*Yellow\*\* = Heat‑Triggered  

&#x20; - \*\*Gray\*\* = No watering day  

\- Tap any day to open details  



\## 3.2 Day Detail View

Displays:

\- Date  

\- Status  

\- Assigned volunteer  

\- Weather info (rain probability, high temp)  

\- Buttons:

&#x20; - \*\*Sign Up\*\*  

&#x20; - \*\*Remove Me\*\*  

&#x20; - \*\*Admin Override\*\*  



\## 3.3 Sign‑Up Flow

\- User taps \*\*Sign Up\*\*

\- Confirmation modal

\- Slot becomes \*\*Filled\*\*

\- Nagging stops



\## 3.4 Remove Me Flow

\- User taps \*\*Remove Me\*\*

\- Confirmation modal

\- Slot becomes \*\*Open\*\*

\- Group notification sent



\## 3.5 Notifications

Users receive:

\- Open slot alerts  

\- Daily nagging (8 AM)  

\- Rain‑day alerts  

\- Heat‑triggered day alerts  

\- Sign‑up confirmations  

\- Removal confirmations  



Nagging suppressed on:

\- Rain days  

\- Filled days  

\- Past days  



\---



\# 4. Weather Automation



\## 4.1 Rain Rule (6 AM)

1\. Fetch rain probability  

2\. If ≥ threshold:

&#x20;  - Mark slot as Rain  

&#x20;  - Set `isRainDay = true`  

&#x20;  - Clear volunteer (if enabled)  

&#x20;  - Notify users  

&#x20;  - Suppress nagging  



\## 4.2 Heat Rule (6 AM)

1\. Fetch high temperature  

2\. If ≥ threshold AND not a rain day:

&#x20;  - Add heat‑triggered slots  

&#x20;  - Mark `isHeatTriggered = true`  

&#x20;  - Notify users  

&#x20;  - Nag until filled  



\---



\# 5. Data Model



\## 5.1 WateringSlot

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



\## 5.2 User

| Field | Type | Description |

|-------|------|-------------|

| id | GUID | Unique user ID |

| name | String | Display name |

| contact | String | Email or phone |

| isAdmin | Boolean | Admin privileges |



\## 5.3 Admin Settings

| Field | Type | Description |

|-------|------|-------------|

| rainThreshold | Number | Default 80% |

| heatThreshold | Number | Default 80°F |

| autoClearOnRain | Boolean | Default true |

| seasonStart | Date | Season start |

| seasonEnd | Date | Season end |

| wateringPattern | Array | \[Mon, Wed, Fri, Sat, Sun] |



\---



\# 6. Automation Logic



\## 6.1 Schedule Generator

\- Generates slots only on M/W/F/S/S  

\- Default values:

&#x20; - status = Open  

&#x20; - isRainDay = false  

&#x20; - isHeatTriggered = false  



\## 6.2 Vacancy Detection

Triggered when a user removes themselves:

\- Notify group that the slot is open  



\## 6.3 Daily Nagging (8 AM)

\- Notify users of all \*\*Open\*\* slots  

\- Skip if:

&#x20; - Rain  

&#x20; - Filled  

&#x20; - Past  



\---



\# 7. UI Structure



\## 7.1 Screens

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



\## 7.2 Calendar Color Coding

\- \*\*Green\*\* = Filled  

\- \*\*Red\*\* = Open  

\- \*\*Blue\*\* = Rain  

\- \*\*Yellow\*\* = Heat‑Triggered  

\- \*\*Gray\*\* = No watering day  



\---



\# 8. Technology Recommendations

This app is optimized for:

\- \*\*Power Apps (Canvas App)\*\*  

\- \*\*Power Automate\*\* for weather checks, nagging, and automation  

\- \*\*Microsoft Lists or Dataverse\*\* for data storage  



\---



\# 9. Status

\*\*Specification: Finalized\*\*  

Ready for implementation.





