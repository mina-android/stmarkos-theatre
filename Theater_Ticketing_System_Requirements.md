# Theater Ticketing & Silent Printing System
## Project Requirements Document

### 1. Project Overview
This project is a lightweight, specialized ticketing system designed for theaters. It intentionally excludes payment processing to focus purely on inventory (seat) management and high-speed, automated label printing. The system must operate on a centralized database accessible by multiple devices, ensuring real-time syncing of available seats. 

### 2. Core Requirements & Workflows

#### A. Initialization Stage (Setup Page)
* **Purpose:** To configure the database for upcoming shows.
* **Features:** 
  * A dedicated setup page to register a new Show (Name, Date, Time).
  * Ability to define multiple seating Zones for each show (e.g., "Balcony", "VIP").
  * Ability to set the total seat capacity for each Zone.

#### B. Dashboard Stage (Monitoring Page)
* **Purpose:** To provide a real-time overview of ticket inventory.
* **Features:** 
  * A data table displaying all initialized shows.
  * Columns must include: Show Name, Date, Time, Zone Name, and Available Seats.
  * Updates in real-time as tickets are printed from any connected device.

#### C. Printing Stage & Silent Print (Ticketing Page)
* **Purpose:** To issue tickets with zero user friction.
* **Features:**
  * User selects a Show and Zone.
  * **Drafting:** The system formats the label exactly as follows:
    * `[Show Name]`
    * `[Show Date] - [Show Time]`
    * `[Zone Name] 0` *(Note: The number '0' is statically appended to the zone name. There are no individual seat numbers).*
  * **Inventory Subtraction:** Subtracts `1` from the available seats for that specific zone.
  * **Silent Printing:** The system must automatically send the formatted label directly to the printer. **There must be no browser print dialogues, no opening PDFs in new tabs, and no manual user confirmation.**

#### D. Auditing & Device Logging
* **Purpose:** To maintain a strict, immutable record of all ticketing actions for accountability.
* **Features:**
  * **Device Registration:** The first time a device opens the app, it must be assigned a name (e.g., "Terminal 1"). The system generates a UUID saved to the device's local storage to identify it in all future requests.
  * **Action Logging:** Every time a ticket is printed, it logs the Show, Zone, Timestamp, Action (e.g., "PRINTED"), and the specific Device UUID/Name that triggered it.
  * **Atomic Transactions:** The database must use strict transactions. The seat subtraction and the audit log creation must execute together. If one fails, the other must roll back to prevent inventory mismatch.

---

### 3. Recommended Technology Stack
To achieve the concurrency requirements and the strict "silent printing" bypass of standard browser security, the following stack is required:

* **Database:** PostgreSQL (Crucial for handling concurrent row-level locking when multiple devices print simultaneously).
* **Backend:** Node.js with Express (or Python FastAPI) for fast I/O and database transaction management.
* **Frontend UI:** React.js or Vue.js for a snappy, single-page application experience across the Setup, Dashboard, and Print pages.
* **Application Wrapper (For Silent Printing):** Electron.js. 
  * *Why:* Standard web browsers block silent printing. Wrapping the React frontend in an Electron desktop app grants access to native OS APIs (like `webContents.print({ silent: true })`), enabling background printing to USB or network label printers. *(Alternative: Web App + QZ Tray).*

---

### 4. Database Schema Requirements

**1. `shows` Table**
* `id` (Primary Key)
* `name` (String)
* `date` (Date)
* `time` (Time)

**2. `zones` Table**
* `id` (Primary Key)
* `show_id` (Foreign Key -> shows.id)
* `zone_name` (String)
* `total_capacity` (Integer)
* `available_seats` (Integer)

**3. `devices` Table**
* `id` (Primary Key - UUID)
* `device_name` (String - assigned at first launch)

**4. `ticket_logs` Table**
* `id` (Primary Key)
* `show_id` (Foreign Key -> shows.id)
* `zone_id` (Foreign Key -> zones.id)
* `device_id` (Foreign Key -> devices.id)
* `action` (String - e.g., "PRINTED")
* `printed_at` (Timestamp)
