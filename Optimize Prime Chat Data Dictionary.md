# MXP Data Dictionary - Query Reference

## Version Control
- **Version**: 1.8.0
- **Last Updated**: 2025-11-07
- **Updated By**: Shetu Shah (shetu.shah@virginvoyages.com)
- **Changes**: Added Person_Charge_Cards table to data dictionary with business definitions for all columns. This table contains credit card and payment card information for Sailors only.

---

# IMPORTANT QUERY GENERATION RULES

## Data Formatting Requirements
- **GUID fields** should be returned in lowercase format
- **Date columns** (without time) should be formatted as YYYY-MM-DD only
- **DateTime columns** (with time) should include the full timestamp
- **CRITICAL**: When requesting chargeId, ALWAYS use `Person_Account.EXTERNAL_ACCOUNT_ID`, NOT `Person_Booking.CHARGE_ID` unless specifically requested otherwise

## SQL Script Requirements
- **ALL UPDATE and DELETE scripts MUST be wrapped in transactions** for data safety
- Use `BEGIN TRANSACTION;` before the update/delete statement
- Use `COMMIT;` after successful execution, or `ROLLBACK;` if issues are found
- Include `@@ROWCOUNT` to show how many rows were affected
- **ALL UPDATE statements MUST include change logging** with the following 3 fields:
  - `CHANGED = 'Y'`
  - `LAST_CHANGE_LOG_ID = CHANGE_TRACKING_CURRENT_VERSION()`
  - `LAST_CHANGED = GETDATE()`
- **READ-ONLY queries should use WITH (NOLOCK) hint** to avoid blocking and improve performance
- Example:
  ```sql
  BEGIN TRANSACTION;
  UPDATE table SET 
      column = value,
      CHANGED = 'Y',
      LAST_CHANGE_LOG_ID = CHANGE_TRACKING_CURRENT_VERSION(),
      LAST_CHANGED = GETDATE()
  WHERE condition;
  PRINT 'Rows updated: ' + CAST(@@ROWCOUNT AS VARCHAR(10));
  COMMIT; -- or ROLLBACK; if issues found
  ```

## Column Definition Tags
- **[Crew]** - Field applies to crew members only
- **[Sailor]** - Field applies to sailors (customers) only  
- **[Crew, Sailor]** - Field applies to both crew members and sailors

## Key Ship Identifiers
- **VAL (Valiant Lady)**: `ORG_UNIT_ID = 4`
- **SCL (Scarlet Lady)**: `ORG_UNIT_ID = 2`
- **RES (Resilient Lady)**: `ORG_UNIT_ID = 5`
- **BRL (Brilliant Lady)**: `ORG_UNIT_ID = 6`
- **Head Office**: `ORG_UNIT_ID = 1`
- **Shipyard**: `ORG_UNIT_ID = 3`

## Common Status Values
- **PERSON_TYPE_ID**: 1 = Sailor, 2 = Crew
- **BOOKING_ARRIVAL_STATUS**: 0 = Not Checked In, 1 = Checked In
- **PERSON_BOOKING_STATUS_ID**: 0 = Pending (OF), 1 = Confirmed (RS), 3 = Cancelled (CN)
- **ACCOUNT_STATUS_ID**: 2 = Active, 3 = Voided
- **REC_DELETED**: 0 = Not deleted, 1 = Deleted

---

# QUERY GENERATION REFERENCE

## Table Relationships
- **Persons** ↔ **Person_Booking**: `Persons.PERSON_ID = Person_Booking.PERSON_ID`
- **Person_Booking** ↔ **Person_Account**: `Person_Booking.PERSON_ID = Person_Account.PERSON_ID`
- **Person_Booking** ↔ **Cruise**: `Person_Booking.CRUISE_ID = Cruise.CRUISE_ID`
- **Person_Booking** ↔ **Org_Units**: `Person_Booking.ORG_UNIT_ID = Org_Units.ORG_UNIT_ID`

## Common Query Patterns

### Get Checked-in Sailors on a Specific Ship
```sql
SELECT p.PERSON_FIRST_NAME, p.PERSON_LAST_NAME, pb.BOOKING_ROOM_NO
FROM Persons p WITH (NOLOCK)
INNER JOIN Person_Booking pb WITH (NOLOCK) ON p.PERSON_ID = pb.PERSON_ID
WHERE p.PERSON_TYPE_ID = 1  -- Sailors only
    AND pb.ORG_UNIT_ID = 4  -- VAL (Valiant Lady)
    AND pb.BOOKING_ARRIVAL_STATUS = 1  -- Checked in
    AND pb.REC_DELETED = 0
    AND p.REC_DELETED = 0
```

### Get Account Information with Charge ID
```sql
SELECT p.PERSON_FIRST_NAME, p.PERSON_LAST_NAME, pa.EXTERNAL_ACCOUNT_ID
FROM Persons p WITH (NOLOCK)
INNER JOIN Person_Account pa WITH (NOLOCK) ON p.PERSON_ID = pa.PERSON_ID
WHERE pa.STATUS_ID = 2  -- Active accounts
    AND pa.REC_DELETED = 0
```

## Important Notes for LLM Query Generation
1. Always filter out deleted records using `REC_DELETED = 0`
2. Use proper JOINs between related tables
3. Format GUIDs as lowercase using `LOWER(column_name)`
4. Format dates as YYYY-MM-DD using `FORMAT(column_name, 'yyyy-MM-dd')`
5. For charge IDs, always use `Person_Account.EXTERNAL_ACCOUNT_ID`
6. Wrap UPDATE/DELETE operations in transactions
7. Include appropriate WHERE clauses to filter by ship, status, etc.
8. **Use WITH (NOLOCK) hint on all tables in read-only SELECT queries** to avoid blocking and improve performance

---
# MXP Data Dictionary - Schema Definitions

## Version Control
- **Version**: 1.0.0
- **Last Updated**: 2025-01-27
- **Updated By**: Data Dictionary Team
- **Changes**: Schema definitions extracted from live database with business definitions

*This data dictionary uses actual column names from the database schema*

*Key corrections made:*

* - Fixed table name: Person_Visa → Person_Visas*
* - Fixed column name mismatches to match actual database schema*
* - Removed non-existent columns*
* - Updated column names to their actual database equivalents*

## Persons

*Core table containing Sailor (customer) information and their associated attributes*

### Columns

DEBUG: Table 'Persons' has 135 total columns, 34 have business definitions
DEBUG: After excluding columns: 102 columns remaining
DEBUG: Final result: 34 columns with business definitions
| COLUMN_NAME                   | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                   | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| PERSON_ID                     | int             | YES           |             0 | [Crew, Sailor] MXP Sailor ID - This is the unique identifier for each sailor in  |
|                               |                 |               |               | the MXP system.                                                                  |
| PERSON_EXTERNAL_ID            | bigint          | YES           |             0 | [Sailor] Seaware Client ID. This is the unique identifier for each sailor in the |
|                               |                 |               |               | Seaware system.                                                                  |
| PERSON_TITLE                  | int             | YES           |             0 | [Crew, Sailor] Title of the sailor (e.g., Mr., Mrs., Ms., etc.)                  |
| PERSON_FIRST_NAME             | varchar(40)     | NO            |             0 | [Crew, Sailor] First name of the sailor or crew member                           |
| PERSON_MIDDLE_NAME            | varchar(40)     | YES           |             0 | [Crew, Sailor] Middle name of the sailor or crew member                          |
| PERSON_LAST_NAME              | varchar(40)     | NO            |             0 | [Crew, Sailor] Last name of the sailor or crew member                            |
| PERSON_GENDER                 | char(1)         | YES           |             0 | [Crew, Sailor] Gender of the sailor or crew member                               |
| PERSON_TYPE_ID                | varchar(2)      | NO            |             0 | [Crew, Sailor] Type of person. Values:  1 = Sailor, 2 = Crew                     |
| PERSON_DOB                    | datetime        | YES           |             0 | [Crew, Sailor] Date of birth of the sailor or crew member. Should be formatted   |
|                               |                 |               |               | as YYYY-MM-DD only.                                                              |
| COUNTRY_OF_RESIDENCE_ID       | int             | YES           |             0 | [Crew, Sailor] ID of the country of residence of the sailor or crew member. FK   |
|                               |                 |               |               | to Countries table.                                                              |
| REC_DELETED                   | bit             | NO            |             0 | [Crew, Sailor] Whether the Person record is deleted or not. Values: 0 = Not      |
|                               |                 |               |               | deleted, 1 = Deleted                                                             |
| CREATED_AT_ID                 | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where it was created. Values: 1 = Head     |
|                               |                 |               |               | Office or Shoreside, 2 = Scarlet Lady (SCL), 3 = Shipyard, 4 = Valiant Lady      |
|                               |                 |               |               | (VAL), 5 = Resilient Lady (RES), 6 = Brilliant Lady (BRL). FK to Org_Units       |
|                               |                 |               |               | table.                                                                           |
| CREATED_BY_ID                 | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the Person record. FK to MXP Users     |
|                               |                 |               |               | table.                                                                           |
| CREATED                       | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the Person record was created.                 |
| LAST_CHANGED                  | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the Person record was last changed. Should be  |
|                               |                 |               |               | set on SQL Update.                                                               |
| CHANGED                       | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record was changed and needs to be consider for  |
|                               |                 |               |               | replication between Head Office and one of the ships. Should be set on SQL       |
|                               |                 |               |               | Update Values: N = No, Y = Yes                                                   |
| GUID                          | uniqueidentifie | NO            |             0 | [Crew, Sailor] GUID of the Person record. For Sailors, this is the VXP guestid.  |
|                               | r               |               |               | For Crew, this is the Apollo Solutions GUID. Should be returned in lowercase     |
|                               |                 |               |               | format.                                                                          |
| PERSON_PIN_CODE               | varchar(200)    | YES           |             0 | [Crew, Sailor] PIN used to authenticate the Sailor at Casino or Retail POS.      |
| PERSON_NATIONALITY_COUNTRY_ID | int             | YES           |             0 | [Crew, Sailor] ID of the country of nationality of the sailor or crew member. FK |
|                               |                 |               |               | to Countries table.                                                              |
| ACTIVE                        | bit             | NO            |             0 | [Crew, Sailor] Whether the Person record is active or not. Values: 0 = Inactive, |
|                               |                 |               |               | 1 = Active                                                                       |
| PERSON_COUNTRY_OF_BIRTH_ID    | int             | YES           |             0 | [Crew, Sailor] ID of the country of birth of the sailor or crew member. FK to    |
|                               |                 |               |               | Countries table.                                                                 |
| USER_ID                       | int             | YES           |             0 | [Crew] FK into MXP Users table.                                                  |
| PERSON_FIRST_STAY             | datetime        | YES           |             0 | [Crew] Start date of a crew member first contract. Can be adjusted for return    |
|                               |                 |               |               | crew continuity of service. Should be formatted as YYYY-MM-DD only.              |
| PERSON_PRIMARY_EMAIL          | varchar(100)    | YES           |             0 | [Crew, Sailor] Primary email address of the sailor. While populated for crew, we |
|                               |                 |               |               | use the email address on the Primary Home Address from the Person_Addresses      |
|                               |                 |               |               | table for crew.                                                                  |
| PERSON_BOOKING_CONTACT_ID     | int             | YES           |             0 | [Crew] ID of the Manning Agent.                                                  |
| PERSON_FIRST_NAME_UNICODE     | nvarchar(40)    | YES           |             0 | [Sailor] This is used by MXP POS to display the account name. For Sailors, this  |
|                               |                 |               |               | is the Preferred Name.                                                           |
| LAST_CHANGE_LOG_ID            | bigint          | YES           |             0 | [Crew, Sailor] Should be updated using a change tracking function on SQL Update. |
| PERSON_FIRST_NAME_PREFERRED   | varchar(40)     | YES           |             0 | [Crew] Preferred first name.                                                     |
| PERSON_USERNAME               | varchar(40)     | YES           |             0 | [Crew] MXP Login ID for MXP system and apps                                      |
| PERSON_PREFERRED_GENDER       | varchar(1)      | YES           |             0 | [Crew] Preferred gender of the crew member.                                      |
| PERSON_LGBTQ_COMMUNITY_STATUS | bit             | YES           |             0 | [Crew] Indicates if the sailor or crew member is part of the LGBTQ+ community.   |
|                               |                 |               |               | Used to invite Crew to events and affinity groups. Values: 0 = No, 1 = Yes       |
| PERSON_RELIGION_IDENTITY_ID   | int             | YES           |             0 | [Crew] Religious affiliation of the crew member. Used to invite Crew to events   |
|                               |                 |               |               | and affinity groups.                                                             |
| ALCOHOL_CHALLENGED            | bit             | NO            |             0 | [Sailor] Blocks Sailor from being able to purchase alcohol. Values: 0 = No, 1 =  |
|                               |                 |               |               | Yes                                                                              |


### Foreign Keys

*No foreign keys found for this table.*

---

## Person_Booking

*Booking information for Sailors, including cruise details, room assignments, and booking status*

### Columns

DEBUG: Table 'Person_Booking' has 82 total columns, 36 have business definitions
DEBUG: After excluding columns: 41 columns remaining
| COLUMN_NAME                      | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:---------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                      | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| PERSON_BOOKING_ID                | int             | YES           |             0 | [Crew, Sailor] Unique identifier for a booking record in MXP.                    |
| PERSON_ID                        | int             | NO            |             0 | [Crew, Sailor] Foreign key to the Persons table, linking the booking to a        |
|                                  |                 |               |               | specific sailor or crew member.                                                  |
| EXTERNAL_BOOKING_ID              | int             | YES           |             0 | [Sailor] Seaware booking ID. This is the unique identifier for each booking in   |
|                                  |                 |               |               | the Seaware system.                                                              |
| ORG_UNIT_ID                      | int             | YES           |             0 | [Crew, Sailor] ID of the ship or organizational unit where the booking is        |
|                                  |                 |               |               | assigned. FK to Org_Units table.                                                 |
| BOOKING_REFERENCE                | varchar(100)    | YES           |             0 | [Sailor] Booking reference number displayed to the sailor and used in customer   |
|                                  |                 |               |               | communications.                                                                  |
| BOOKING_ROOM_NO                  | varchar(50)     | YES           |             0 | [Crew, Sailor] Cabin/room number assigned to the sailor or crew member. Format:  |
|                                  |                 |               |               | Deck, 3-digit room number, and side (A: Port, Z: Starboard, M: Middle)           |
| CRUISE_ID                        | int             | YES           |             0 | [Crew, Sailor] ID of the cruise voyage. FK to Cruise table.                      |
| ARRIVAL_DATE                     | datetime        | YES           |             0 | [Crew, Sailor] Date and time when the sailor or crew member is scheduled to      |
|                                  |                 |               |               | arrive. Should include full timestamp.                                           |
| DEPARTURE_DATE                   | datetime        | YES           |             0 | [Crew, Sailor] Date and time when the sailor or crew member is scheduled to      |
|                                  |                 |               |               | depart. Should include full timestamp.                                           |
| EMBARKATION_CITY_ID              | int             | YES           |             0 | [Crew, Sailor] ID of the city where the sailor or crew member will embark. FK to |
|                                  |                 |               |               | Cities table.                                                                    |
| DEBARKATION_CITY_ID              | int             | YES           |             0 | [Crew, Sailor] ID of the city where the sailor or crew member will debark. FK to |
|                                  |                 |               |               | Cities table.                                                                    |
| REC_DELETED                      | bit             | NO            |             0 | [Crew, Sailor] Whether the booking record is deleted. Values: 0 = Not deleted, 1 |
|                                  |                 |               |               | = Deleted                                                                        |
| CREATED_AT_ID                    | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the booking was created. Values: 1 = |
|                                  |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED_BY_ID                    | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the booking record. FK to MXP Users    |
|                                  |                 |               |               | table.                                                                           |
| CREATED                          | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the booking record was created.                |
| LAST_CHANGED                     | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the booking record was last modified.          |
| CHANGED                          | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                                  |                 |               |               | Yes                                                                              |
| GUID                             | uniqueidentifie | NO            |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking. FK to |
|                                  | r               |               |               | VXP reservationguest table, VXP reservationguestid. Should be returned in        |
|                                  |                 |               |               | lowercase format.                                                                |
| BOOKING_ARRIVAL_STATUS           | bit             | NO            |             0 | [Crew, Sailor] Whether the person has Checked in. Values: 0 = Not Checked In, 1  |
|                                  |                 |               |               | = Checked In                                                                     |
| POSITION_ID                      | int             | YES           |             0 | [Crew] ID of the crew member's position/role for this booking. FK to Positions   |
|                                  |                 |               |               | table.                                                                           |
| POSITION_ORG_UNIT_DETAIL_ID      | int             | YES           |             0 | [Crew] ID of the specific department/unit position details. FK to                |
|                                  |                 |               |               | Position_Org_Unit_Details table.                                                 |
| BOOKING_CONTACT_ID               | int             | YES           |             0 | [Crew] ID of the manning agency or booking contact. FK to Booking_Contacts       |
|                                  |                 |               |               | table.                                                                           |
| PERSON_BOOKING_STATUS_ID         | int             | YES           |             0 | [Crew, Sailor] Current status of the booking. Values: 0 = Pending (OF),1 =       |
|                                  |                 |               |               | Confirmed (RS), 3 = Cancelled (CN)                                               |
| BOOKING_VIP_STATUS_ID            | int             | YES           |             0 | [Sailor] VIP status level of the booking. Values: VIP1 = MegaRockstar, VIP2 =    |
|                                  |                 |               |               | Rockstar, VIP3 = Commercially Important, VIP4 = Commercially Important 2, VIP5 = |
|                                  |                 |               |               | Important                                                                        |
| BOOKING_ACCESS_STATUS_ID         | int             | YES           |             0 | [Crew, Sailor] Gangway status of the person, whether they are on the ship or     |
|                                  |                 |               |               | not. Values: 0 = Ashore, 1 = Onboard                                             |
| NONE_REVENUE_BOOKING             | bit             | YES           |             0 | [Sailor] Indicates if this is a complimentary booking. Values: 0 = Revenue       |
|                                  |                 |               |               | booking, 1 = Non-revenue booking                                                 |
| MANIFEST_TYPE                    | char(1)         | YES           |             0 | [Crew, Sailor] Type of manifest entry. Values: P = Passenger, E = Employee, I =  |
|                                  |                 |               |               | Invisible (not on manifest)                                                      |
| USER_ID                          | int             | YES           |             0 | [Crew] Associated MXP user account ID if the crew member has system access. FK   |
|                                  |                 |               |               | to MXP Users table.                                                              |
| USER_ROLE_ID                     | int             | YES           |             0 | [Crew] Role assigned to the crew member in MXP for this booking. FK to           |
|                                  |                 |               |               | User_Roles table.                                                                |
| LAST_CHANGE_LOG_ID               | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this booking.           |
| CHARGE_ID                        | bigint          | YES           |             0 | [Sailor] ID of the primary charge account for this booking. NOTE: When           |
|                                  |                 |               |               | requesting chargeId, always use Person_Account.EXTERNAL_ACCOUNT_ID instead of    |
|                                  |                 |               |               | this field unless specifically requested otherwise.                              |
| ROUTE_CHARGES_TO_PERSON_ID       | bigint          | YES           |             0 | [Sailor] ID of the person to whom charges should be routed.                      |
| SUPERVISOR_GROUP_ID              | int             | YES           |             0 | [Crew] Primary supervisor group assignment. This is the group they are an        |
|                                  |                 |               |               | employee of and should not be null                                               |
| SUPERVISOR_GROUP_ID_2            | int             | YES           |             0 | [Crew] Secondary supervisor group assignment. This is the group they are the     |
|                                  |                 |               |               | supervisor of and can be null.                                                   |
| GUEST_TYPE_ID                    | int             | YES           |             0 | [Sailor] Type of guest. FK to Guest_Types table.                                 |
| DOOR_LOCK_INTERFACE_CODE         | varchar(40)     | YES           |             0 |                                                                                  |
| EARLY_BOARDING_BOOKING           | bit             | YES           |             0 |                                                                                  |
| BOOKING_COMMENT_UNICODE          | nvarchar(1000)  | YES           |             0 |                                                                                  |
| BOOKING_CHECK_IN_COMMENT_UNICODE | nvarchar(200)   | YES           |             0 |                                                                                  |
| BOOKING_SOURCE_UNICODE           | nvarchar(200)   | YES           |             0 |                                                                                  |


### Foreign Keys

| FK_Name                   | Table_Name     | Column_Name   | Referenced_Table   | Referenced_Column   |
|:--------------------------|:---------------|:--------------|:-------------------|:--------------------|
| FK_Person_Booking_Persons | Person_Booking | PERSON_ID     | Persons            | PERSON_ID           |


---

## Cruise

*Core table containing cruise voyage information, including dates, ship assignment, and itinerary details*

### Columns

DEBUG: Table 'Cruise' has 126 total columns, 17 have business definitions
DEBUG: After excluding columns: 125 columns remaining
DEBUG: Final result: 17 columns with business definitions
| COLUMN_NAME                   | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                   | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| CRUISE_ID                     | int             | YES           |             0 | [Crew, Sailor] Unique identifier for a cruise voyage.                            |
| CRUISE_NUMBER                 | varchar(25)     | NO            |             0 | [Crew, Sailor] Business name for the voyage in format: "XXYYMMDDNNN" where XX =  |
|                               |                 |               |               | 2-char Ship Code (e.g., VL for Valiant Lady), YYMMDD = Start Date, NNN = Sailing |
|                               |                 |               |               | length in nights (e.g., 5N) followed by Seaware package code for repeat          |
|                               |                 |               |               | itineraries.                                                                     |
| ORG_UNIT_ID                   | int             | NO            |             0 | [Crew, Sailor] ID of the ship operating this cruise. FK to Org_Units table.      |
| START_DATE                    | datetime        | YES           |             0 | [Crew, Sailor] Date and time when the cruise begins. Should include full         |
|                               |                 |               |               | timestamp.                                                                       |
| END_DATE                      | datetime        | YES           |             0 | [Crew, Sailor] Date and time when the cruise ends. Should include full           |
|                               |                 |               |               | timestamp.                                                                       |
| CRUISE_STATUS                 | char(1)         | YES           |             0 | [Crew, Sailor] Current status of the cruise.                                     |
| DELETED                       | bit             | NO            |             0 | [Crew, Sailor] Whether the cruise record is deleted. Values: 0 = Not deleted, 1  |
|                               |                 |               |               | = Deleted                                                                        |
| CREATED_AT_ID                 | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the cruise was created. Values: 1 =  |
|                               |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED                       | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the cruise record was created.                 |
| LAST_CHANGED                  | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the cruise record was last modified.           |
| CHANGED                       | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                               |                 |               |               | Yes                                                                              |
| GUID                          | uniqueidentifie | YES           |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.       |
|                               | r               |               |               | Should be returned in lowercase format.                                          |
| CREATED_BY_ID                 | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the cruise record. FK to MXP Users     |
|                               |                 |               |               | table.                                                                           |
| CRUISE_TYPE_ID                | int             | YES           |             0 | [Crew, Sailor] Type of cruise. FK to Cruise_Types table.                         |
| LAST_CHANGE_LOG_ID            | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this cruise.            |
| CRUISE_ITINERARY_DEVIATION_ID | int             | YES           |             0 | [Crew, Sailor] ID of the planned itinerary. FK to Cruise_Itineraries table.      |


### Foreign Keys

*No foreign keys found for this table.*

---

## Org_Units

*Organizational structure table containing ships, offices, and other organizational units*

### Columns

DEBUG: Table 'Org_Units' has 308 total columns, 11 have business definitions
DEBUG: After excluding columns: 308 columns remaining
DEBUG: Final result: 11 columns with business definitions
| COLUMN_NAME           | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:----------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER           | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| ORG_UNIT_ID           | int             | YES           |             0 | [Crew, Sailor] Unique identifier for an organizational unit. Values: 1 = Head    |
|                       |                 |               |               | Office (HO), 2 = Scarlet Lady (SC), 3 = Shipyard (SY), 4 = Valiant Lady (VL), 5  |
|                       |                 |               |               | = Resilient Lady (RS), 6 = Brilliant Lady (BR)                                   |
| ORG_UNIT_NAME         | varchar(40)     | NO            |             0 | [Crew, Sailor] Full name of the organizational unit. This is the name of the     |
|                       |                 |               |               | ship or office.                                                                  |
| ORG_UNIT_ABBREVIATION | varchar(6)      | YES           |             0 | [Crew, Sailor] Two-character code for the organizational unit. Values: HO = Head |
|                       |                 |               |               | Office, SC = Scarlet Lady, VL = Valiant Lady, RS = Resilient Lady, BR =          |
|                       |                 |               |               | Brilliant Lady, SY = Shipyard                                                    |
| CREATED_AT_ID         | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the record was created. Values: 1 =  |
|                       |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED               | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the record was created.                        |
| LAST_CHANGED          | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the record was last modified.                  |
| CHANGED               | varchar(1)      | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                       |                 |               |               | Yes                                                                              |
| GUID                  | uniqueidentifie | YES           |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.       |
|                       | r               |               |               | Should be returned in lowercase format.                                          |
| CREATED_BY_ID         | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the record. FK to MXP Users table.     |
| LAST_CHANGE_LOG_ID    | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record.                            |


### Foreign Keys

| FK_Name                     | Table_Name   | Column_Name      | Referenced_Table   | Referenced_Column   |
|:----------------------------|:-------------|:-----------------|:-------------------|:--------------------|
| FK_Org_Units_Org_Structure  | Org_Units    | ORG_STRUCTURE_ID | Org_Structure      | ORG_STRUCTURE_ID    |
| FK_Org_Units_Org_Company_ID | Org_Units    | ORG_COMPANY_ID   | Org_Companies      | ORG_COMPANY_ID      |


---

## Person_Passport

*Passport information for Sailors and Crew members, including passport numbers, issue dates, and expiry dates*

### Columns

DEBUG: Table 'Person_Passport' has 32 total columns, 17 have business definitions
DEBUG: After excluding columns: 32 columns remaining
DEBUG: Final result: 17 columns with business definitions
| COLUMN_NAME              | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:-------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER              | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| PERSON_PASSPORT_ID       | int             | YES           |             0 | [Crew, Sailor] Unique identifier for a passport record.                          |
| PERSON_ID                | int             | NO            |             0 | [Crew, Sailor] Foreign key to the Persons table, linking the passport to a       |
|                          |                 |               |               | specific sailor or crew member.                                                  |
| PASSPORT_NUMBER          | varchar(30)     | YES           |             0 | [Crew, Sailor] Passport number of the sailor or crew member.                     |
| PASSPORT_ISSUED_COUNTRY  | int             | YES           |             0 | [Crew, Sailor] ID of the country that issued the passport. FK to Countries       |
|                          |                 |               |               | table.                                                                           |
| PASSPORT_ISSUED_DATE     | datetime        | YES           |             0 | [Crew, Sailor] Date when the passport was issued. Should be formatted as YYYY-   |
|                          |                 |               |               | MM-DD only.                                                                      |
| PASSPORT_EXPIRATION_DATE | datetime        | YES           |             0 | [Crew, Sailor] Date when the passport expires. Should be formatted as YYYY-MM-DD |
|                          |                 |               |               | only.                                                                            |
| IS_PRIMARY_PASSPORT      | bit             | NO            |             0 | [Crew, Sailor] Whether this passport record is marked as the primary passport    |
|                          |                 |               |               | for the person. Values: 0 = Not primary, 1 = Primary                             |
| REC_DELETED              | bit             | NO            |             0 | [Crew, Sailor] Whether the passport record is deleted. Values: 0 = Not deleted,  |
|                          |                 |               |               | 1 = Deleted                                                                      |
| CREATED_AT_ID            | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the passport was created. Values: 1  |
|                          |                 |               |               | = Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                  |
| CREATED_BY_ID            | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the passport record. FK to MXP Users   |
|                          |                 |               |               | table.                                                                           |
| CREATED                  | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the passport record was created.               |
| LAST_CHANGED             | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the passport record was last modified.         |
| CHANGED                  | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                          |                 |               |               | Yes                                                                              |
| GUID                     | uniqueidentifie | NO            |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.       |
|                          | r               |               |               | Should be returned in lowercase format.                                          |
| PASSPORT_TYPE_ID         | int             | NO            |             0 | [Crew, Sailor] Type of passport. FK to Passport_Types table.                     |
| LAST_CHANGE_LOG_ID       | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this passport.          |


### Foreign Keys

| FK_Name                    | Table_Name      | Column_Name   | Referenced_Table   | Referenced_Column   |
|:---------------------------|:----------------|:--------------|:-------------------|:--------------------|
| FK_Person_Passport_Persons | Person_Passport | PERSON_ID     | Persons            | PERSON_ID           |


---

## Person_Visas

*Visa information for Sailors and Crew members, including visa numbers, types, and status*

### Columns

DEBUG: Table 'Person_Visas' has 27 total columns, 27 have business definitions
DEBUG: After excluding columns: 26 columns remaining
DEBUG: Final result: 26 columns with business definitions
| COLUMN_NAME                | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:---------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| PERSON_VISA_ID             | int             | YES           |             0 | [Crew, Sailor] Unique identifier for a visa record.                              |
| PERSON_PASSPORT_ID         | int             | YES           |             0 | [Crew, Sailor] Foreign key to the Person_Passport table, linking the visa to a   |
|                            |                 |               |               | specific passport.                                                               |
| VISA_NAME                  | varchar(50)     | YES           |             0 | [Crew, Sailor] Name or description of the visa.                                  |
| VISA_ISSUED_COUNTRY_ID     | int             | YES           |             0 | [Crew, Sailor] ID of the country that issued the visa. FK to Countries table.    |
| VISA_ISSUED_CITY_NAME      | varchar(50)     | YES           |             0 | [Crew, Sailor] Name of the city where the visa was issued.                       |
| VISA_ISSUED_DATE           | datetime        | YES           |             0 | [Crew, Sailor] Date when the visa was issued. Should be formatted as YYYY-MM-DD  |
|                            |                 |               |               | only.                                                                            |
| VISA_EXPIRATION_DATE       | datetime        | YES           |             0 | [Crew, Sailor] Date when the visa expires. Should be formatted as YYYY-MM-DD     |
|                            |                 |               |               | only.                                                                            |
| REC_DELETED                | bit             | NO            |             0 | [Crew, Sailor] Whether the visa record is deleted. Values: 0 = Not deleted, 1 =  |
|                            |                 |               |               | Deleted                                                                          |
| CREATED_AT_ID              | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the visa was created. Values: 1 =    |
|                            |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED_BY_ID              | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the visa record. FK to MXP Users       |
|                            |                 |               |               | table.                                                                           |
| CREATED                    | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the visa record was created.                   |
| LAST_CHANGED               | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the visa record was last modified.             |
| CHANGED                    | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                            |                 |               |               | Yes                                                                              |
| GUID                       | uniqueidentifie | NO            |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.       |
|                            | r               |               |               | Should be returned in lowercase format.                                          |
| VISA_NAME_ID               | int             | YES           |             0 | [Crew, Sailor] ID of the visa name type. FK to Visa_Name_Types table.            |
| VISA_NUMBER                | varchar(30)     | YES           |             0 | [Crew, Sailor] Visa number of the sailor or crew member.                         |
| VISA_IMAGE                 | image(214748364 | YES           |             0 | [Crew, Sailor] Image data of the visa document.                                  |
|                            | 7)              |               |               |                                                                                  |
| VISA_IMAGE_EXTENSION       | varchar(10)     | YES           |             0 | [Crew, Sailor] File extension of the visa image.                                 |
| VISA_ENTRY_TYPE            | char(1)         | YES           |             0 | [Crew, Sailor] Type of visa entry. Values: S = Single, M = Multiple              |
| VISA_STATUS_ID             | int             | YES           |             0 | [Crew, Sailor] Current status of the visa. FK to Visa_Status table.              |
| LAST_CHANGE_LOG_ID         | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this visa.              |
| HASHBYTES                  | varchar(250)    | YES           |             0 | [Crew, Sailor] Hash value for data integrity checking.                           |
| VISA_ELECTRONIC_OR_STICKER | int             | YES           |             0 | [Crew, Sailor] Whether the visa is electronic or sticker type.                   |
| VISA_INTERFACED            | datetime        | YES           |             0 | [Crew, Sailor] Date and time when the visa was interfaced with external systems. |
| PERSON_VISA_DOCUMENT_URL   | varchar(300)    | YES           |             0 | [Crew, Sailor] URL or path to the visa document file.                            |


### Foreign Keys

| FK_Name                         | Table_Name   | Column_Name        | Referenced_Table   | Referenced_Column   |
|:--------------------------------|:-------------|:-------------------|:-------------------|:--------------------|
| FK_Person_Visas_Person_Passport | Person_Visas | PERSON_PASSPORT_ID | Person_Passport    | PERSON_PASSPORT_ID  |


---

## Person_Account

*Account information for Sailors and Crew members, including balances, limits, and account status*

### Columns

DEBUG: Table 'Person_Account' has 30 total columns, 16 have business definitions
DEBUG: After excluding columns: 30 columns remaining
DEBUG: Final result: 16 columns with business definitions
| COLUMN_NAME               | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:--------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER               | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| PERSON_ACCOUNT_ID         | int             | YES           |             0 | [Crew, Sailor] Unique identifier for an account record.                          |
| PERSON_ID                 | int             | NO            |             0 | [Crew, Sailor] Foreign key to the Persons table, linking the account to a        |
|                           |                 |               |               | specific sailor or crew member.                                                  |
| ORG_UNIT_ID               | int             | NO            |             0 | [Crew, Sailor] ID of the ship or organizational unit where the account is        |
|                           |                 |               |               | active. FK to Org_Units table.                                                   |
| STATUS_ID                 | int             | NO            |             0 | [Crew, Sailor] Status of the account. Values: 2 = Active, 3 = Voided             |
| REC_DELETED               | bit             | NO            |             0 | [Crew, Sailor] Whether the account record is deleted. Values: 0 = Not deleted, 1 |
|                           |                 |               |               | = Deleted                                                                        |
| CREATED_AT_ID             | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the account was created. Values: 1 = |
|                           |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED_BY_ID             | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the account record. FK to MXP Users    |
|                           |                 |               |               | table.                                                                           |
| CREATED                   | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the account record was created.                |
| LAST_CHANGED              | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the account record was last modified.          |
| CHANGED                   | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                           |                 |               |               | Yes                                                                              |
| GUID                      | uniqueidentifie | NO            |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.       |
|                           | r               |               |               | Should be returned in lowercase format.                                          |
| PERSON_ACCOUNT_MAX_AMOUNT | numeric         | YES           |             0 | [Crew, Sailor] Credit limit for the account.                                     |
| EXTERNAL_ACCOUNT_ID       | bigint          | YES           |             0 | [Crew, Sailor] External account identifier from VXP system. This is the chargeId |
|                           |                 |               |               | for the account.                                                                 |
| LAST_CHANGE_LOG_ID        | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this account.           |
| PERSON_ACCOUNT_BALANCE    | numeric         | YES           |             0 | [Crew, Sailor] Current balance of the account.                                   |


### Foreign Keys

*No foreign keys found for this table.*

---

## Person_Account_Items

*Individual account transactions and items for Sailors and Crew members*

### Columns

DEBUG: Table 'Person_Account_Items' has 63 total columns, 63 have business definitions
DEBUG: After excluding columns: 63 columns remaining
DEBUG: Final result: 63 columns with business definitions
| COLUMN_NAME                       | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                            |
|:----------------------------------|:----------------|:--------------|--------------:|:-------------------------------------------------------------------------------|
| ROW_COUNTER                       | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                      |
| PERSON_ACCOUNT_DETAIL_ID          | bigint          | YES           |             0 | [Crew, Sailor] Unique identifier for an account item record.                   |
| PERSON_ACCOUNT_ID                 | int             | NO            |             0 | [Crew, Sailor] Foreign key to the Person_Account table, linking the item to a  |
|                                   |                 |               |               | specific account.                                                              |
| PERIOD_ID                         | int             | NO            |             0 | [Crew, Sailor] ID of the accounting period for this item.                      |
| PERIOD_TYPE_ID                    | char(1)         | NO            |             0 | [Crew, Sailor] Type of accounting period. Values: D = Daily, W = Weekly, M =   |
|                                   |                 |               |               | Monthly                                                                        |
| ORG_STRUCTURE_ID                  | int             | YES           |             0 | [Crew, Sailor] ID of the organizational structure. FK to Org_Structure table.  |
| IM_ID                             | int             | YES           |             0 | [Crew, Sailor] ID of the item master. FK to Item_Master table.                 |
| ACCOUNT_RECORD_TYPE_ID            | int             | NO            |             0 | [Crew, Sailor] Type of account record. FK to Account_Record_Types table.       |
| ACCOUNT_RECORD_CATEGORY_ID        | int             | YES           |             0 | [Crew, Sailor] Category of the account record. FK to Account_Record_Categories |
|                                   |                 |               |               | table.                                                                         |
| ACCOUNT_RECORD_DESCRIPTION        | varchar(200)    | YES           |             0 | [Crew, Sailor] Description of the account item.                                |
| ACCOUNT_SOURCE_RECORD_ID          | bigint          | YES           |             0 | [Crew, Sailor] ID of the source record that generated this account item.       |
| ACCOUNT_SOURCE_TYPE_ID            | int             | YES           |             0 | [Crew, Sailor] Type of source record. FK to Account_Source_Types table.        |
| QUANTITY                          | numeric         | YES           |             0 | [Crew, Sailor] Quantity of the item.                                           |
| MEASUREMENT_UNIT_ID               | int             | YES           |             0 | [Crew, Sailor] ID of the measurement unit. FK to Measurement_Units table.      |
| CURRENCY_ID                       | int             | NO            |             0 | [Crew, Sailor] ID of the currency used for this transaction. FK to Currencies  |
|                                   |                 |               |               | table.                                                                         |
| CREDIT_AMOUNT                     | numeric         | YES           |             0 | [Crew, Sailor] Credit amount for this account item.                            |
| DEBIT_AMOUNT                      | numeric         | YES           |             0 | [Crew, Sailor] Debit amount for this account item.                             |
| DISCOUNT_AMOUNT                   | numeric         | YES           |             0 | [Crew, Sailor] Discount amount applied to this item.                           |
| DISCOUNT_COMMENT                  | varchar(200)    | YES           |             0 | [Crew, Sailor] Comment explaining the discount applied.                        |
| SUPPLY_TYPE_ID                    | int             | YES           |             0 | [Crew, Sailor] Type of supply. FK to Supply_Types table.                       |
| SUPPLY_FROM_ID                    | int             | YES           |             0 | [Crew, Sailor] ID of the supply source. FK to Supply_From table.               |
| SUPPLY_TRANSFER_ID                | int             | YES           |             0 | [Crew, Sailor] ID of the supply transfer. FK to Supply_Transfers table.        |
| COMMENT                           | varchar(240)    | YES           |             0 | [Crew, Sailor] Additional comments for this account item.                      |
| ROUTED_FROM_ACCOUNT_ID            | int             | YES           |             0 | [Crew, Sailor] ID of the account this item was routed from.                    |
| STATUS_ID                         | int             | NO            |             0 | [Crew, Sailor] Status of the account item. FK to Account_Item_Status table.    |
| COMPANY_ID                        | int             | YES           |             0 | [Crew, Sailor] ID of the company. FK to Companies table.                       |
| BUSINESS_UNIT_ID                  | int             | YES           |             0 | [Crew, Sailor] ID of the business unit. FK to Business_Units table.            |
| SITE_ID                           | int             | YES           |             0 | [Crew, Sailor] ID of the site. FK to Sites table.                              |
| COST_CENTER_ID                    | int             | YES           |             0 | [Crew, Sailor] ID of the cost center. FK to Cost_Centers table.                |
| ACCOUNT_ID                        | int             | YES           |             0 | [Crew, Sailor] ID of the general ledger account. FK to Accounts table.         |
| PRODUCT_CODE_ID                   | int             | YES           |             0 | [Crew, Sailor] ID of the product code. FK to Product_Codes table.              |
| CLIENT_ID                         | int             | YES           |             0 | [Crew, Sailor] ID of the client. FK to Clients table.                          |
| REC_DELETED                       | bit             | NO            |             0 | [Crew, Sailor] Whether the account item record is deleted. Values: 0 = Not     |
|                                   |                 |               |               | deleted, 1 = Deleted                                                           |
| CREATED_AT_ID                     | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the item was created. Values: 1 =  |
|                                   |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                  |
| CREATED_BY_ID                     | int             | YES           |             0 | [Crew, Sailor] ID of the user who created the account item. FK to MXP Users    |
|                                   |                 |               |               | table.                                                                         |
| CREATED                           | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the account item record was created.         |
| LAST_CHANGED                      | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the account item record was last modified.   |
| CHANGED                           | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =  |
|                                   |                 |               |               | Yes                                                                            |
| GUID                              | uniqueidentifie | NO            |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.     |
|                                   | r               |               |               | Should be returned in lowercase format.                                        |
| INVOICE_NUMBER                    | int             | YES           |             0 | [Crew, Sailor] Invoice number associated with this account item.               |
| ORG_UNIT_QUICK_CODE               | varchar(50)     | YES           |             0 | [Crew, Sailor] Quick code for the organizational unit.                         |
| BUSINESS_DAY                      | datetime        | YES           |             0 | [Crew, Sailor] Business day for this account item.                             |
| PRINT                             | bit             | NO            |             0 | [Crew, Sailor] Whether this item should be printed on statements.              |
| VOIDED_FROM_ACCOUNT_ITEM_ID       | bigint          | YES           |             0 | [Crew, Sailor] ID of the account item this was voided from.                    |
| ORG_UNIT_QUICK_CODE_ID            | int             | YES           |             0 | [Crew, Sailor] ID of the organizational unit quick code.                       |
| SYNCHRONIZED                      | datetime        | YES           |             0 | [Crew, Sailor] Date and time when this item was synchronized.                  |
| COMMISSION_PERSON_ID              | int             | YES           |             0 | [Crew, Sailor] ID of the person who earned commission on this item.            |
| COMMISSION_AMOUNT                 | numeric         | YES           |             0 | [Crew, Sailor] Commission amount for this item.                                |
| EXTERNAL_REFERENCE                | varchar(50)     | YES           |             0 | [Crew, Sailor] External reference number for this item.                        |
| VAT_PERCENTAGE                    | numeric         | YES           |             0 | [Crew, Sailor] VAT percentage applied to this item.                            |
| VAT_CALCULATION_TYPE              | varchar(1)      | YES           |             0 | [Crew, Sailor] Type of VAT calculation.                                        |
| VAT_INVOICE_NUMBER                | varchar(100)    | YES           |             0 | [Crew, Sailor] VAT invoice number for this item.                               |
| LAST_CHANGE_LOG_ID                | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this account item.    |
| EXTRA_FIELD_STRING_1              | varchar(200)    | YES           |             0 | [Crew, Sailor] Extra field string 1 for additional data.                       |
| EXTRA_FIELD_STRING_2              | varchar(200)    | YES           |             0 | [Crew, Sailor] Extra field string 2 for additional data.                       |
| EXTRA_FIELD_STRING_3              | varchar(200)    | YES           |             0 | [Crew, Sailor] Extra field string 3 for additional data.                       |
| EXTRA_FIELD_STRING_4              | varchar(200)    | YES           |             0 | [Crew, Sailor] Extra field string 4 for additional data.                       |
| EXTRA_FIELD_STRING_5              | varchar(200)    | YES           |             0 | [Crew, Sailor] Extra field string 5 for additional data.                       |
| VAT_INVOICE_NUMBER_GENERATED      | datetime        | YES           |             0 | [Crew, Sailor] Date and time when VAT invoice number was generated.            |
| VAT_CURRENCY_EXCHANGE_RATE        | numeric         | YES           |             0 | [Crew, Sailor] Currency exchange rate for VAT calculations.                    |
| VAT_CURRENCY_ID                   | int             | YES           |             0 | [Crew, Sailor] ID of the currency used for VAT calculations.                   |
| VAT_CONFIGURATION_INSTALLATION_ID | int             | YES           |             0 | [Crew, Sailor] ID of the VAT configuration installation.                       |
| VAT_SAF_T_SIGNATURE               | varchar(2000)   | YES           |             0 | [Crew, Sailor] SAF-T signature for VAT compliance.                             |


### Foreign Keys

*No foreign keys found for this table.*

---

## Person_Charge_Cards

*Credit card and payment card information for Sailors, including card numbers, billing addresses, encryption data, and payment processing details*

### Columns

DEBUG: Table 'Person_Charge_Cards' has 46 total columns, 46 have business definitions
DEBUG: Final result: 46 columns with business definitions
| COLUMN_NAME                   | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                   | int             | NO            |             1 | [Sailor] Primary key for the table.                                              |
| PERSON_CHARGE_CARD_ID         | int             | YES           |             0 | [Sailor] Unique identifier for a charge card record.                             |
| PERSON_ID                     | int             | NO            |             0 | [Sailor] Foreign key to the Persons table, linking the charge card to a specific |
|                               |                 |               |               | sailor.                                                                          |
| CHARGE_CARD_TYPE_ID           | int             | NO            |             0 | [Sailor] Type of charge card. FK to Charge_Card_Types table.                     |
| CHARGE_CARD_NUMBER            | varchar(35)     | YES           |             0 | [Sailor] Charge card number. This field may contain encrypted or masked card     |
|                               |                 |               |               | numbers.                                                                         |
| CHARGE_CARD_EXPIRATION_DATE   | datetime        | YES           |             0 | [Sailor] Date when the charge card expires. Should be formatted as YYYY-MM-DD    |
|                               |                 |               |               | only.                                                                            |
| CHARGE_CARD_CODE              | varchar(10)     | YES           |             0 | [Sailor] Security code (CVV/CVC) for the charge card.                            |
| PRE_APPROVED_AMOUNT           | numeric         | YES           |             0 | [Sailor] Pre-approved amount for the charge card.                                |
| NAME_ON_CARD                  | varchar(60)     | YES           |             0 | [Sailor] Name of the cardholder as it appears on the charge card.                |
| BILLING_ADDRESS_1             | varchar(50)     | YES           |             0 | [Sailor] First line of the billing address for the charge card.                  |
| BILLING_ADDRESS_2             | varchar(50)     | YES           |             0 | [Sailor] Second line of the billing address for the charge card.                 |
| BILLING_ADDRESS_3             | varchar(50)     | YES           |             0 | [Sailor] Third line of the billing address for the charge card.                  |
| BILLING_CITY_NAME             | varchar(50)     | YES           |             0 | [Sailor] City name for the billing address.                                      |
| BILLING_POSTAL_CODE           | varchar(20)     | YES           |             0 | [Sailor] Postal/ZIP code for the billing address.                                |
| BILLING_STATE                 | varchar(50)     | YES           |             0 | [Sailor] State or province for the billing address.                              |
| BILLING_COUNTRY_ID            | int             | YES           |             0 | [Sailor] ID of the country for the billing address. FK to Countries table.       |
| REC_DELETED                   | bit             | NO            |             0 | [Sailor] Whether the charge card record is deleted. Values: 0 = Not deleted, 1 = |
|                               |                 |               |               | Deleted                                                                          |
| CREATED_AT_ID                 | int             | YES           |             0 | [Sailor] ID of the MXP instance where the charge card was created. Values: 1 =   |
|                               |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED_BY_ID                 | int             | YES           |             0 | [Sailor] ID of the user who created the charge card record. FK to MXP Users      |
|                               |                 |               |               | table.                                                                           |
| CREATED                       | datetime        | NO            |             0 | [Sailor] Date and time when the charge card record was created.                  |
| LAST_CHANGED                  | datetime        | NO            |             0 | [Sailor] Date and time when the charge card record was last modified.            |
| CHANGED                       | char(1)         | NO            |             0 | [Sailor] Indicates if the record needs replication. Values: N = No, Y = Yes      |
| GUID                          | uniqueidentifie | NO            |             0 | [Sailor] Unique identifier used for system integration and tracking. Should be   |
|                               | r               |               |               | returned in lowercase format.                                                    |
| CHARGE_CARD_TRACK1            | varchar(200)    | YES           |             0 | [Sailor] Track 1 data from the magnetic stripe of the charge card.               |
| CHARGE_CARD_TRACK2            | varchar(200)    | YES           |             0 | [Sailor] Track 2 data from the magnetic stripe of the charge card.               |
| CHARGE_CARD_TRACK3            | varchar(200)    | YES           |             0 | [Sailor] Track 3 data from the magnetic stripe of the charge card.               |
| CHARGE_CARD_SIGNATURE         | image(214748364 | YES           |             0 | [Sailor] Binary image data of the cardholder signature.                          |
|                               | 7)              |               |               |                                                                                  |
| CHARGE_CARD_SIGNATURE_DATE    | datetime        | YES           |             0 | [Sailor] Date when the signature was captured. Should be formatted as YYYY-MM-DD |
|                               |                 |               |               | only.                                                                            |
| CHARGE_CARD_SEQUENCE          | int             | YES           |             0 | [Sailor] Sequence number for the charge card, used when a sailor has multiple    |
|                               |                 |               |               | cards.                                                                           |
| CHARGE_CARD_MAXIMUM_AMOUNT    | numeric         | YES           |             0 | [Sailor] Maximum amount limit for the charge card.                               |
| INVOICE_NUMBER                | int             | YES           |             0 | [Sailor] Invoice number associated with the charge card.                         |
| ACTIVE                        | bit             | YES           |             0 | [Sailor] Whether the charge card record is active. Values: 0 = Inactive, 1 =     |
|                               |                 |               |               | Active                                                                           |
| CREATED_BY_SWIPING            | bit             | YES           |             0 | [Sailor] Whether the charge card record was created by swiping the card. Values: |
|                               |                 |               |               | 0 = No, 1 = Yes                                                                  |
| CHARGE_CARD_P2P               | varchar(4096)   | YES           |             0 | [Sailor] P2P (Point-to-Point) encrypted data for the charge card.                |
| CHARGE_CARD_EXTERNAL_ID       | bigint          | YES           |             0 | [Sailor] External identifier for the charge card from external payment systems.  |
| CHARGE_CARD_ENCODED_DATA      | image(214748364 | YES           |             0 | [Sailor] Binary encoded data for the charge card.                                |
|                               | 7)              |               |               |                                                                                  |
| CHARGE_CARD_KSN_CODE          | varchar(200)    | YES           |             0 | [Sailor] Key Serial Number (KSN) code used for encryption/decryption of the      |
|                               |                 |               |               | charge card data.                                                                |
| CHARGE_CARD_TOKEN             | varchar(100)    | YES           |             0 | [Sailor] Tokenized value for the charge card, used for secure payment            |
|                               |                 |               |               | processing.                                                                      |
| CHARGE_CARD_PURGED            | datetime        | YES           |             0 | [Sailor] Date and time when the charge card data was purged for security         |
|                               |                 |               |               | compliance.                                                                      |
| CHARGE_CARD_NUMBER_ENCRYPTED  | varchar(500)    | YES           |             0 | [Sailor] Encrypted charge card number.                                           |
| CHARGE_CARD_KEY_ID            | int             | YES           |             0 | [Sailor] ID of the encryption key used for the charge card. FK to encryption key |
|                               |                 |               |               | management system.                                                               |
| LAST_CHANGE_LOG_ID            | bigint          | YES           |             0 | [Sailor] ID of the last change tracking record for this charge card.             |
| HASHBYTES                     | varchar(250)    | YES           |             0 | [Sailor] Hash value for data integrity checking.                                 |
| CHECK_IN_SYNC                 | varchar(1)      | YES           |             0 | [Sailor] Synchronization status for check-in processes.                          |
| CHARGE_CARD_DCC_CURRENCY_ID   | int             | YES           |             0 | [Sailor] ID of the currency used for Dynamic Currency Conversion (DCC). FK to    |
|                               |                 |               |               | Currencies table.                                                                |
| CHARGE_CARD_DCC_EXCHANGE_RATE | numeric         | YES           |             0 | [Sailor] Exchange rate used for Dynamic Currency Conversion (DCC).               |


### Foreign Keys

| FK_Name                        | Table_Name          | Column_Name   | Referenced_Table   | Referenced_Column   |
|:-------------------------------|:--------------------|:--------------|:-------------------|:--------------------|
| FK_Person_Charge_Cards_Persons | Person_Charge_Cards | PERSON_ID     | Persons            | PERSON_ID           |


---

## Person_Amenities

*Amenity access information for Sailors, including access dates and status*

### Columns

DEBUG: Table 'Person_Amenities' has 29 total columns, 29 have business definitions
DEBUG: After excluding columns: 29 columns remaining
DEBUG: Final result: 29 columns with business definitions
| COLUMN_NAME                    | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:-------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                    | int             | NO            |             1 | [Sailor] Primary key for the table.                                              |
| PERSON_AMENITY_ID              | int             | YES           |             0 | [Sailor] Unique identifier for an amenity record.                                |
| PERSON_ID                      | int             | NO            |             0 | [Sailor] Foreign key to the Persons table, linking the amenity to a specific     |
|                                |                 |               |               | sailor.                                                                          |
| PERSON_AMENITY_TYPE_ID         | int             | NO            |             0 | [Sailor] Type of amenity. FK to Amenity_Types table.                             |
| PERSON_AMENITY_COMMENT         | varchar(200)    | YES           |             0 | [Sailor] Comment or description for the amenity record, including special notes  |
|                                |                 |               |               | such as "BAR TAB (Onboard)" for onboard bar tab amenities.                       |
| AMENITY_DELIVERY_DATE          | datetime        | YES           |             0 | [Sailor] Date when the amenity should be delivered. Should be formatted as YYYY- |
|                                |                 |               |               | MM-DD only.                                                                      |
| AMENTIY_DELIVERY_TIME          | datetime        | YES           |             0 | [Sailor] Time when the amenity should be delivered.                              |
| AMENITY_DELIVERY_ON_BY         | char(1)         | YES           |             0 | [Sailor] Method of amenity delivery. Values: O = Onboard, S = Shore              |
| AMENITY_DELIVERY_PLACE         | varchar(200)    | YES           |             0 | [Sailor] Place where the amenity should be delivered.                            |
| REC_DELETED                    | bit             | NO            |             0 | [Sailor] Whether the amenity record is deleted. Values: 0 = Not deleted, 1 =     |
|                                |                 |               |               | Deleted                                                                          |
| CREATED                        | datetime        | NO            |             0 | [Sailor] Date and time when the amenity record was created.                      |
| CREATED_BY_ID                  | int             | YES           |             0 | [Sailor] ID of the user who created the amenity record. FK to MXP Users table.   |
| CREATED_AT_ID                  | int             | YES           |             0 | [Sailor] ID of the MXP instance where the amenity was created. Values: 1 = Head  |
|                                |                 |               |               | Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                         |
| CHANGED                        | char(1)         | NO            |             0 | [Sailor] Indicates if the record needs replication. Values: N = No, Y = Yes      |
| LAST_CHANGED                   | datetime        | NO            |             0 | [Sailor] Date and time when the amenity record was last modified.                |
| GUID                           | uniqueidentifie | NO            |             0 | [Sailor] Unique identifier used for system integration and tracking. Should be   |
|                                | r               |               |               | returned in lowercase format.                                                    |
| PERSON_AMENITY_EXTERNAL_ID     | bigint          | YES           |             0 | [Sailor] External identifier for the amenity from external systems.              |
| PERSON_AMENITY_AMOUNT          | numeric         | YES           |             0 | [Sailor] Amount associated with the amenity.                                     |
| ORG_UNIT_ID                    | int             | YES           |             0 | [Sailor] ID of the ship or organizational unit where the amenity is available.   |
|                                |                 |               |               | FK to Org_Units table.                                                           |
| AMENITY_DELIVERED_ON           | datetime        | YES           |             0 | [Sailor] Date when the amenity was actually delivered.                           |
| AMENITY_DELIVERED_BY           | varchar(50)     | YES           |             0 | [Sailor] Name or identifier of the person who delivered the amenity.             |
| AMENITY_PERIOD                 | varchar(20)     | YES           |             0 | [Sailor] Period for which the amenity is valid.                                  |
| AMENITY_PRINTED_DATE           | datetime        | YES           |             0 | [Sailor] Date when the amenity was printed.                                      |
| AMENITY_APPLIED_DATE           | datetime        | YES           |             0 | [Sailor] Date when the amenity was applied.                                      |
| PERSON_AMENITY_QUANTITY        | numeric         | YES           |             0 | [Sailor] Quantity of the amenity.                                                |
| LAST_CHANGE_LOG_ID             | bigint          | YES           |             0 | [Sailor] ID of the last change tracking record for this amenity.                 |
| HASHBYTES                      | varchar(250)    | YES           |             0 | [Sailor] Hash value for data integrity checking.                                 |
| PERSON_AMENITY_CURRENCY_ID     | int             | YES           |             0 | [Sailor] ID of the currency used for the amenity amount.                         |
| PERSON_AMENITY_COMMENT_UNICODE | nvarchar(200)   | YES           |             0 | [Sailor] Unicode comment or notes for the amenity record.                        |


### Foreign Keys

| FK_Name                     | Table_Name       | Column_Name   | Referenced_Table   | Referenced_Column   |
|:----------------------------|:-----------------|:--------------|:-------------------|:--------------------|
| FK_Person_Amenities_Persons | Person_Amenities | PERSON_ID     | Persons            | PERSON_ID           |


---

## Person_Images

*Image files and metadata for Sailors and Crew members, including profile photos, ID photos, and other document images*

### Columns

DEBUG: Table 'Person_Images' has 16 total columns, 16 have business definitions
DEBUG: After excluding columns: 16 columns remaining
DEBUG: Final result: 16 columns with business definitions
| COLUMN_NAME                           | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:--------------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                           | int             | NO            |             1 | [Crew, Sailor] Primary key for the table.                                        |
| PERSON_IMAGE_ID                       | int             | YES           |             0 | [Crew, Sailor] Unique identifier for an image record.                            |
| PERSON_ID                             | int             | NO            |             0 | [Crew, Sailor] Foreign key to the Persons table, linking the image to a specific |
|                                       |                 |               |               | sailor or crew member.                                                           |
| IMAGE                                 | varbinary(-1)   | YES           |             0 | [Crew, Sailor] Binary data of the image file.                                    |
| REC_DELETED                           | bit             | NO            |             0 | [Crew, Sailor] Whether the image record is deleted. Values: 0 = Not deleted, 1 = |
|                                       |                 |               |               | Deleted                                                                          |
| CREATED_AT_ID                         | int             | YES           |             0 | [Crew, Sailor] ID of the MXP instance where the image was created. Values: 1 =   |
|                                       |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED_BY_ID                         | int             | YES           |             0 | [Crew, Sailor] ID of the user who uploaded the image. FK to MXP Users table.     |
| CREATED                               | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the image record was created.                  |
| LAST_CHANGED                          | datetime        | NO            |             0 | [Crew, Sailor] Date and time when the image record was last modified.            |
| CHANGED                               | char(1)         | NO            |             0 | [Crew, Sailor] Indicates if the record needs replication. Values: N = No, Y =    |
|                                       |                 |               |               | Yes                                                                              |
| GUID                                  | uniqueidentifie | NO            |             0 | [Crew, Sailor] Unique identifier used for system integration and tracking.       |
|                                       | r               |               |               | Should be returned in lowercase format.                                          |
| IMAGE_TEMPLATE                        | image(214748364 | YES           |             0 | [Crew, Sailor] Template image data for processing.                               |
|                                       | 7)              |               |               |                                                                                  |
| LAST_CHANGE_LOG_ID                    | bigint          | YES           |             0 | [Crew, Sailor] ID of the last change tracking record for this image.             |
| HASHBYTES                             | varchar(250)    | YES           |             0 | [Crew, Sailor] Hash value for data integrity checking.                           |
| CHECK_IN_SYNC                         | varchar(1)      | YES           |             0 | [Crew, Sailor] Synchronization status for check-in processes.                    |
| IMAGE_FACIAL_RECOGNITION_MATCH_STATUS | varchar(30)     | YES           |             0 | [Crew, Sailor] Status of facial recognition matching for this image.             |


### Foreign Keys

| FK_Name                  | Table_Name    | Column_Name   | Referenced_Table   | Referenced_Column   |
|:-------------------------|:--------------|:--------------|:-------------------|:--------------------|
| FK_Person_Images_Persons | Person_Images | PERSON_ID     | Persons            | PERSON_ID           |


---

## Person_Special_Requests

*Special requests and accommodations for Sailors, including dietary, accessibility, medical, and other personalized needs*

### Columns

DEBUG: Table 'Person_Special_Requests' has 23 total columns, 23 have business definitions
DEBUG: After excluding columns: 23 columns remaining
DEBUG: Final result: 23 columns with business definitions
| COLUMN_NAME                            | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:---------------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                            | int             | NO            |             1 | [Sailor] Primary key for the table.                                              |
| PERSON_SPECIAL_REQUEST_ID              | int             | YES           |             0 | [Sailor] Unique identifier for a special request record.                         |
| PERSON_ID                              | int             | NO            |             0 | [Sailor] Foreign key to the Persons table, linking the special request to a      |
|                                        |                 |               |               | specific sailor.                                                                 |
| PERSON_SPECIAL_REQUEST_EXTERNAL_ID     | bigint          | YES           |             0 | [Sailor] External identifier for the special request from external systems.      |
| PERSON_SPECIAL_REQUEST_TYPE_ID         | int             | NO            |             0 | [Sailor] Type of special request. FK to Special_Request_Types table. Values: 1 = |
|                                        |                 |               |               | Dietary, 2 = Accessibility, 3 = Medical, 4 = Religious, 5 = Celebrations, 6 =    |
|                                        |                 |               |               | Other                                                                            |
| PERSON_SPECIAL_REQUEST_DESCRIPTION     | varchar(300)    | NO            |             0 | [Sailor] Detailed description of the special request.                            |
| PERSON_SPECIAL_REQUEST_COMMENT         | text(2147483647 | YES           |             0 | [Sailor] Additional comments or notes for the special request.                   |
|                                        | )               |               |               |                                                                                  |
| PERSON_SPECIAL_REQUEST_DATE            | datetime        | YES           |             0 | [Sailor] Date when the special request should be applied (e.g., birthday date,   |
|                                        |                 |               |               | anniversary date). Should be formatted as YYYY-MM-DD only.                       |
| REC_DELETED                            | bit             | NO            |             0 | [Sailor] Whether the special request record is deleted. Values: 0 = Not deleted, |
|                                        |                 |               |               | 1 = Deleted                                                                      |
| CREATED_AT_ID                          | int             | YES           |             0 | [Sailor] ID of the MXP instance where the special request was created. Values: 1 |
|                                        |                 |               |               | = Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                  |
| CREATED_BY_ID                          | int             | YES           |             0 | [Sailor] ID of the user who created the special request. FK to MXP Users table.  |
| CREATED                                | datetime        | NO            |             0 | [Sailor] Date and time when the special request record was created.              |
| LAST_CHANGED                           | datetime        | NO            |             0 | [Sailor] Date and time when the special request record was last modified.        |
| CHANGED                                | char(1)         | NO            |             0 | [Sailor] Indicates if the record needs replication. Values: N = No, Y = Yes      |
| GUID                                   | uniqueidentifie | NO            |             0 | [Sailor] Unique identifier used for system integration and tracking. Should be   |
|                                        | r               |               |               | returned in lowercase format.                                                    |
| ORG_UNIT_ID                            | int             | YES           |             0 | [Sailor] ID of the ship or organizational unit where the special request is      |
|                                        |                 |               |               | applicable. FK to Org_Units table.                                               |
| PERSON_SPECIAL_REQUEST_QUANTITY        | numeric         | YES           |             0 | [Sailor] Quantity associated with the special request.                           |
| PERSON_SPECIAL_REQUEST_AMOUNT          | numeric         | YES           |             0 | [Sailor] Amount associated with the special request.                             |
| SPECIAL_REQUEST_APPLIED_DATE           | datetime        | YES           |             0 | [Sailor] Date when the special request was actually applied/fulfilled. Should be |
|                                        |                 |               |               | formatted as YYYY-MM-DD only.                                                    |
| LAST_CHANGE_LOG_ID                     | bigint          | YES           |             0 | [Sailor] ID of the last change tracking record for this special request.         |
| HASHBYTES                              | varchar(250)    | YES           |             0 | [Sailor] Hash value for data integrity checking.                                 |
| SPECIAL_REQUEST_APPLIED_BY             | varchar(100)    | YES           |             0 | [Sailor] Name or identifier of the person who applied/fulfilled the special      |
|                                        |                 |               |               | request.                                                                         |
| PERSON_SPECIAL_REQUEST_COMMENT_UNICODE | nvarchar(-1)    | YES           |             0 | [Sailor] Unicode comment or notes for the special request.                       |


### Foreign Keys

*No foreign keys found for this table.*

---

## Person_Appraisal

*Performance appraisal records for Crew members, including ratings, feedback, goals, and approval workflow tracking*

### Columns

DEBUG: Table 'Person_Appraisal' has 49 total columns, 49 have business definitions
DEBUG: After excluding columns: 49 columns remaining
DEBUG: Final result: 49 columns with business definitions
| COLUMN_NAME                     | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                             |
|:--------------------------------|:----------------|:--------------|--------------:|:--------------------------------------------------------------------------------|
| ROW_COUNTER                     | int             | NO            |             1 | [Crew] Primary key for the table.                                               |
| PERSON_APPRAISAL_ID             | int             | YES           |             0 | [Crew] Unique identifier for an appraisal record.                               |
| PERSON_ID                       | int             | NO            |             0 | [Crew] Foreign key to the Persons table, linking the appraisal to a specific    |
|                                 |                 |               |               | crew member.                                                                    |
| APPRAISER_STATUS_ID             | int             | NO            |             0 | [Crew] Status of the appraiser in the appraisal process. FK to Appraiser_Status |
|                                 |                 |               |               | table.                                                                          |
| APPRAISER_1_USER_ID             | int             | YES           |             0 | [Crew] ID of the first appraiser. FK to MXP Users table.                        |
| APPRAISER_2_USER_ID             | int             | YES           |             0 | [Crew] ID of the second appraiser. FK to MXP Users table.                       |
| APPRAISER_3_USER_ID             | int             | YES           |             0 | [Crew] ID of the third appraiser. FK to MXP Users table.                        |
| APPRAISER_4_USER_ID             | int             | YES           |             0 | [Crew] ID of the fourth appraiser. FK to MXP Users table.                       |
| REC_DELETED                     | bit             | NO            |             0 | [Crew] Whether the appraisal record is deleted. Values: 0 = Not deleted, 1 =    |
|                                 |                 |               |               | Deleted                                                                         |
| CREATED_AT_ID                   | int             | YES           |             0 | [Crew] ID of the MXP instance where the appraisal was created. Values: 1 = Head |
|                                 |                 |               |               | Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                        |
| CREATED_BY_ID                   | int             | YES           |             0 | [Crew] ID of the user who created the appraisal record. FK to MXP Users table.  |
| CREATED                         | datetime        | NO            |             0 | [Crew] Date and time when the appraisal record was created.                     |
| LAST_CHANGED                    | datetime        | NO            |             0 | [Crew] Date and time when the appraisal record was last modified.               |
| CHANGED                         | char(1)         | NO            |             0 | [Crew] Indicates if the record needs replication. Values: N = No, Y = Yes       |
| GUID                            | uniqueidentifie | NO            |             0 | [Crew] Unique identifier used for system integration and tracking. Should be    |
|                                 | r               |               |               | returned in lowercase format.                                                   |
| APPRAISAL_DATE                  | datetime        | NO            |             0 | [Crew] Date when the appraisal was conducted. Should be formatted as YYYY-MM-DD |
|                                 |                 |               |               | only.                                                                           |
| APPRAISAL_TYPE_ID               | int             | YES           |             0 | [Crew] Type of appraisal. FK to Appraisal_Types table.                          |
| APPRAISER_DOCUMENT              | image(214748364 | YES           |             0 | [Crew] Binary data of the appraisal document.                                   |
|                                 | 7)              |               |               |                                                                                 |
| POSITION_ID                     | int             | YES           |             0 | [Crew] ID of the crew member's position for this appraisal. FK to Positions     |
|                                 |                 |               |               | table.                                                                          |
| APPRAISAL_TEMPLATE_ID           | int             | YES           |             0 | [Crew] ID of the appraisal template used. FK to Appraisal_Templates table.      |
| APPRAISER_DOCUMENT_EXTENSION    | varchar(10)     | YES           |             0 | [Crew] File extension of the appraisal document.                                |
| PERSON_BOOKING_ID               | int             | YES           |             0 | [Crew] ID of the booking associated with this appraisal. FK to Person_Booking   |
|                                 |                 |               |               | table.                                                                          |
| LAST_CHANGE_LOG_ID              | bigint          | YES           |             0 | [Crew] ID of the last change tracking record for this appraisal.                |
| APPRAISAL_REVIEWER_COMMENT      | varchar(1000)   | YES           |             0 | [Crew] Comments from the reviewer about the appraisal.                          |
| APPRAISAL_EMPLOYEE_COMMENT      | varchar(1000)   | YES           |             0 | [Crew] Comments from the employee about their own performance.                  |
| APPRAISAL_AVERAGE_RATING        | numeric         | YES           |             0 | [Crew] Average rating score for the appraisal.                                  |
| APPRAISAL_GOAL_1                | varchar(1000)   | YES           |             0 | [Crew] First performance goal for the employee.                                 |
| APPRAISAL_FEEDBACK_1            | varchar(1000)   | YES           |             0 | [Crew] Feedback related to the first goal.                                      |
| APPRAISAL_GOAL_2                | varchar(1000)   | YES           |             0 | [Crew] Second performance goal for the employee.                                |
| APPRAISAL_FEEDBACK_2            | varchar(1000)   | YES           |             0 | [Crew] Feedback related to the second goal.                                     |
| APPRAISAL_GOAL_3                | varchar(1000)   | YES           |             0 | [Crew] Third performance goal for the employee.                                 |
| APPRAISAL_FEEDBACK_3            | varchar(1000)   | YES           |             0 | [Crew] Feedback related to the third goal.                                      |
| APPRAISAL_APPROVER_COMMENT      | varchar(1000)   | YES           |             0 | [Crew] Comments from the approver about the appraisal.                          |
| APPRAISER_FINAL_USER_ID         | int             | YES           |             0 | [Crew] ID of the final appraiser who completed the appraisal. FK to MXP Users   |
|                                 |                 |               |               | table.                                                                          |
| APPRAISAL_STATUS_ID             | int             | YES           |             0 | [Crew] Current status of the appraisal. FK to Appraisal_Status table.           |
| APPRAISAL_PERIOD_ID             | int             | YES           |             0 | [Crew] ID of the appraisal period. FK to Appraisal_Periods table.               |
| PROPOSED_RETURN_STATUS_ID       | int             | YES           |             0 | [Crew] Proposed return status for the crew member. FK to Return_Status table.   |
| APPRAISAL_ACKNOWLED_BY_EMPLOYEE | datetime        | YES           |             0 | [Crew] Date and time when the employee acknowledged the appraisal.              |
| APPRAISER_1_REVIEWED            | datetime        | YES           |             0 | [Crew] Date and time when appraiser 1 reviewed the appraisal.                   |
| APPRAISER_1_SIGNED              | datetime        | YES           |             0 | [Crew] Date and time when appraiser 1 signed the appraisal.                     |
| APPRAISER_2_REVIEWED            | datetime        | YES           |             0 | [Crew] Date and time when appraiser 2 reviewed the appraisal.                   |
| APPRAISER_2_SIGNED              | datetime        | YES           |             0 | [Crew] Date and time when appraiser 2 signed the appraisal.                     |
| APPRAISER_3_REVIEWED            | datetime        | YES           |             0 | [Crew] Date and time when appraiser 3 reviewed the appraisal.                   |
| APPRAISER_3_SIGNED              | datetime        | YES           |             0 | [Crew] Date and time when appraiser 3 signed the appraisal.                     |
| APPRAISER_4_REVIEWED            | datetime        | YES           |             0 | [Crew] Date and time when appraiser 4 reviewed the appraisal.                   |
| APPRAISER_4_SIGNED              | datetime        | YES           |             0 | [Crew] Date and time when appraiser 4 signed the appraisal.                     |
| APPRAISAL_STRENGTH_1            | varchar(150)    | YES           |             0 | [Crew] First strength identified in the appraisal.                              |
| APPRAISAL_STRENGTH_2            | varchar(150)    | YES           |             0 | [Crew] Second strength identified in the appraisal.                             |
| APPRAISAL_STRENGTH_3            | varchar(150)    | YES           |             0 | [Crew] Third strength identified in the appraisal.                              |


### Foreign Keys

*No foreign keys found for this table.*

---

## Person_Warning

*Disciplinary warning records for Crew members, including warning types, dates, descriptions, and documentation. Warnings are linked to crew bookings where the warning date falls between the crew member's arrival_date and departure_date for that booking.*

### Columns

DEBUG: Table 'Person_Warning' has 21 total columns, 21 have business definitions
DEBUG: After excluding columns: 21 columns remaining
DEBUG: Final result: 21 columns with business definitions
| COLUMN_NAME                     | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:--------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                     | int             | NO            |             1 | [Crew] Primary key for the table.                                                |
| PERSON_WARNING_ID               | int             | YES           |             0 | [Crew] Unique identifier for a warning record.                                   |
| PERSON_ID                       | int             | NO            |             0 | [Crew] Foreign key to the Persons table, linking the warning to a specific crew  |
|                                 |                 |               |               | member.                                                                          |
| PERSON_WARNING_TYPE_ID          | int             | NO            |             0 | [Crew] Type of warning issued. FK to Warning_Types table.                        |
| PERSON_WARNING_DATE             | datetime        | NO            |             0 | [Crew] Date when the warning was issued. Should be formatted as YYYY-MM-DD only. |
|                                 |                 |               |               | This date must fall between the crew member's arrival_date and departure_date    |
|                                 |                 |               |               | for the associated booking.                                                      |
| PERSON_WARNING_TEXT             | text(2147483647 | NO            |             0 | [Crew] Detailed text description of the warning.                                 |
|                                 | )               |               |               |                                                                                  |
| REC_DELETED                     | bit             | NO            |             0 | [Crew] Whether the warning record is deleted. Values: 0 = Not deleted, 1 =       |
|                                 |                 |               |               | Deleted                                                                          |
| CREATED_AT_ID                   | int             | YES           |             0 | [Crew] ID of the MXP instance where the warning was created. Values: 1 = Head    |
|                                 |                 |               |               | Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                         |
| CREATED_BY_ID                   | int             | YES           |             0 | [Crew] ID of the user who created the warning record. FK to MXP Users table.     |
| CREATED                         | datetime        | NO            |             0 | [Crew] Date and time when the warning record was created.                        |
| LAST_CHANGED                    | datetime        | NO            |             0 | [Crew] Date and time when the warning record was last modified.                  |
| CHANGED                         | char(1)         | NO            |             0 | [Crew] Indicates if the record needs replication. Values: N = No, Y = Yes        |
| GUID                            | uniqueidentifie | NO            |             0 | [Crew] Unique identifier used for system integration and tracking. Should be     |
|                                 | r               |               |               | returned in lowercase format.                                                    |
| PERSON_WARNING_COMMENT          | text(2147483647 | YES           |             0 | [Crew] Additional comments or notes about the warning.                           |
|                                 | )               |               |               |                                                                                  |
| PERSON_WARNING_DESCRIPTION_ID   | int             | YES           |             0 | [Crew] ID of the warning description template. FK to Warning_Descriptions table. |
| PERSON_WARNING_DOCUMENT         | image(214748364 | YES           |             0 | [Crew] Binary data of the warning document.                                      |
|                                 | 7)              |               |               |                                                                                  |
| PERSON_WARNING_NUMBER           | varchar(50)     | YES           |             0 | [Crew] Warning number or reference for tracking purposes.                        |
| PERSON_WARNING_CATEGORY         | varchar(1)      | YES           |             0 | [Crew] Category of the warning. Values: C = Dismissal, W = Written Warning       |
| LAST_CHANGE_LOG_ID              | bigint          | YES           |             0 | [Crew] ID of the last change tracking record for this warning.                   |
| PERSON_WARNING_EXPIRATION_DATE  | datetime        | YES           |             0 | [Crew] Date when the warning expires or is no longer valid. Should be formatted  |
|                                 |                 |               |               | as YYYY-MM-DD only.                                                              |
| PERSON_WARNING_EMPLOYEE_COMMENT | varchar(250)    | YES           |             0 | [Crew] Comments from the employee about the warning.                             |


### Foreign Keys

*No foreign keys found for this table.*

---

## Person_Courses

*Training and certification records for Crew members, including course completion, certificates, expiration dates, and training progress tracking*

### Columns

DEBUG: Table 'Person_Courses' has 56 total columns, 56 have business definitions
DEBUG: After excluding columns: 56 columns remaining
DEBUG: Final result: 56 columns with business definitions
| COLUMN_NAME                            | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:---------------------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                            | int             | NO            |             1 | [Crew] Primary key for the table.                                                |
| PERSON_COURSE_ID                       | int             | YES           |             0 | [Crew] Unique identifier for a course record.                                    |
| PERSON_ID                              | int             | YES           |             0 | [Crew] Foreign key to the Persons table, linking the course to a specific crew   |
|                                        |                 |               |               | member.                                                                          |
| COURSE_CATEGORY_ID                     | int             | NO            |             0 | [Crew] ID of the course category. FK to Course_Categories table.                 |
| COURSE_CERTIFICATE_NO                  | varchar(50)     | YES           |             0 | [Crew] Certificate number for the course completion.                             |
| COURSE_DATE                            | datetime        | NO            |             0 | [Crew] Date when the course was taken. Should include full timestamp.            |
| COURSE_LOCATION                        | varchar(40)     | NO            |             0 | [Crew] Location where the course was conducted.                                  |
| COURSE_RESULT                          | varchar(40)     | YES           |             0 | [Crew] Result of the course (e.g., Pass, Fail, Incomplete).                      |
| COURSE_COMMENT                         | varchar(1000)   | YES           |             0 | [Crew] Additional comments or notes about the course.                            |
| COURSE_VALID_FROM                      | datetime        | YES           |             0 | [Crew] Date when the course certification becomes valid. Should include full     |
|                                        |                 |               |               | timestamp.                                                                       |
| COURSE_VALID_TO                        | datetime        | YES           |             0 | [Crew] Date when the course certification expires. Should include full           |
|                                        |                 |               |               | timestamp.                                                                       |
| COURSE_IS_REQUIRED                     | int             | YES           |             0 | [Crew] Whether this course is required for the crew member. Values: 0 = Not      |
|                                        |                 |               |               | required, 1 = Required                                                           |
| REC_DELETED                            | bit             | NO            |             0 | [Crew] Whether the course record is deleted. Values: 0 = Not deleted, 1 =        |
|                                        |                 |               |               | Deleted                                                                          |
| CREATED                                | datetime        | NO            |             0 | [Crew] Date and time when the course record was created.                         |
| CREATED_AT_ID                          | int             | YES           |             0 | [Crew] ID of the MXP instance where the course was created. Values: 1 = Head     |
|                                        |                 |               |               | Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                         |
| CREATED_BY_ID                          | int             | YES           |             0 | [Crew] ID of the user who created the course record. FK to MXP Users table.      |
| CHANGED                                | char(1)         | NO            |             0 | [Crew] Indicates if the record needs replication. Values: N = No, Y = Yes        |
| LAST_CHANGED                           | datetime        | NO            |             0 | [Crew] Date and time when the course record was last modified.                   |
| GUID                                   | uniqueidentifie | NO            |             0 | [Crew] Unique identifier used for system integration and tracking. Should be     |
|                                        | r               |               |               | returned in lowercase format.                                                    |
| COURSE_EXPIRATION_TYPE_ID              | int             | YES           |             0 | [Crew] ID of the expiration type for the course. FK to Course_Expiration_Types   |
|                                        |                 |               |               | table.                                                                           |
| COURSE_DOCUMENT                        | image(214748364 | YES           |             0 | [Crew] Binary data of the course certificate or document.                        |
|                                        | 7)              |               |               |                                                                                  |
| COURSE_DOCUMENT_EXTENSION              | varchar(10)     | YES           |             0 | [Crew] File extension of the course document.                                    |
| COURSE_FLAG_STATE_ID                   | int             | YES           |             0 | [Crew] ID of the flag state for the course. FK to Flag_States table.             |
| ACTIVE_STATUS                          | bit             | YES           |             0 | [Crew] Whether the course record is active. Values: 0 = Inactive, 1 = Active     |
| COURSE_COUNTRY_ID                      | int             | YES           |             0 | [Crew] ID of the country where the course was taken. FK to Countries table.      |
| COURSE_EXPERIENCE_LEVEL_ID             | int             | YES           |             0 | [Crew] ID of the experience level required for the course. FK to                 |
|                                        |                 |               |               | Experience_Levels table.                                                         |
| LAST_CHANGE_LOG_ID                     | bigint          | YES           |             0 | [Crew] ID of the last change tracking record for this course.                    |
| TRAINING_SCHEDULE_ID                   | int             | YES           |             0 | [Crew] ID of the training schedule. FK to Training_Schedules table.              |
| COURSE_ATTENDANCE_STATUS               | bit             | YES           |             0 | [Crew] Whether the crew member attended the course. Values: 0 = Did not attend,  |
|                                        |                 |               |               | 1 = Attended                                                                     |
| COURSE_PASSED                          | bit             | YES           |             0 | [Crew] Whether the crew member passed the course. Values: 0 = Failed, 1 = Passed |
| USER_ID                                | int             | YES           |             0 | [Crew] ID of the user associated with the course record. FK to MXP Users table.  |
| APPLICANT_ID                           | int             | YES           |             0 | [Crew] ID of the applicant for the course.                                       |
| TRAINING_PROGRAM_COURSE_ID             | int             | YES           |             0 | [Crew] ID of the training program course. FK to Training_Program_Courses table.  |
| COURSE_DATE_STARTED                    | datetime        | YES           |             0 | [Crew] Date when the course was started. Should include full timestamp.          |
| COURSE_DATE_COMPLETED                  | datetime        | YES           |             0 | [Crew] Date when the course was completed. Should include full timestamp.        |
| COURSE_ASSIGNED_BY_RULE_ID             | int             | YES           |             0 | [Crew] ID of the rule that assigned this course. FK to Course_Assignment_Rules   |
|                                        |                 |               |               | table.                                                                           |
| COURSE_COMPLETION_DATE_TYPE_ID         | int             | YES           |             0 | [Crew] ID of the completion date type. FK to Course_Completion_Date_Types table. |
| PERSON_BOOKING_ID                      | int             | YES           |             0 | [Crew] ID of the booking associated with this course. FK to Person_Booking       |
|                                        |                 |               |               | table.                                                                           |
| PERSON_COURSE_PROGRESS                 | float           | NO            |             0 | [Crew] Progress percentage of the course completion (0-100).                     |
| PERSON_COURSE_STATUS_ID                | int             | NO            |             0 | [Crew] Current status of the course for the crew member. FK to                   |
|                                        |                 |               |               | Person_Course_Status table.                                                      |
| PERSON_COURSE_MANUALLY_EXTENDED        | bit             | NO            |             0 | [Crew] Whether the course validity was manually extended. Values: 0 = Not        |
|                                        |                 |               |               | extended, 1 = Extended                                                           |
| COURSE_RATING                          | int             | YES           |             0 | [Crew] Rating given to the course by the crew member.                            |
| PERSON_COURSE_EXPIRATION_NOTIFICATION  | bit             | YES           |             0 | [Crew] Whether an expiration notification was sent. Values: 0 = Not sent, 1 =    |
|                                        |                 |               |               | Sent                                                                             |
| COURSE_ASSIGNMENT_VALID_FROM           | datetime        | YES           |             0 | [Crew] Date when the course assignment becomes valid. Should include full        |
|                                        |                 |               |               | timestamp.                                                                       |
| COURSE_ASSIGNMENT_VALID_TO             | datetime        | YES           |             0 | [Crew] Date when the course assignment expires. Should include full timestamp.   |
| COURSE_EXPIRATION_MONTHS               | int             | YES           |             0 | [Crew] Number of months until the course expires.                                |
| CONTACT_NAME_ID                        | int             | YES           |             0 | [Crew] ID of the contact person for the course. FK to Contact_Names table.       |
| PERSON_COURSE_ASSIGNMENT_NOTIFICATION  | bit             | YES           |             0 | [Crew] Whether an assignment notification was sent. Values: 0 = Not sent, 1 =    |
|                                        |                 |               |               | Sent                                                                             |
| PERSON_COURSE_SHOW_COMPLETION_MESSAGE  | int             | YES           |             0 | [Crew] Whether to show completion message. Values: 0 = Don't show, 1 = Show      |
| FAVOURITE                              | bit             | YES           |             0 | [Crew] Whether this course is marked as favorite by the crew member. Values: 0 = |
|                                        |                 |               |               | Not favorite, 1 = Favorite                                                       |
| PERSON_COURSE_CERTIFICATE_NOTIFICATION | bit             | YES           |             0 | [Crew] Whether a certificate notification was sent. Values: 0 = Not sent, 1 =    |
|                                        |                 |               |               | Sent                                                                             |
| REC_DELETED_REASON                     | nvarchar(300)   | YES           |             0 | [Crew] Reason for deletion of the course record.                                 |
| COURSE_RATING_DATE                     | datetime        | YES           |             0 | [Crew] Date when the course was rated. Should include full timestamp.            |
| ARCHIVED                               | bit             | NO            |             0 | [Crew] Whether the course record is archived. Values: 0 = Not archived, 1 =      |
|                                        |                 |               |               | Archived                                                                         |
| COURSE_DOCUMENT_URL                    | varchar(300)    | YES           |             0 | [Crew] URL or path to the course document file.                                  |
| COURSE_EXTERNAL_ID                     | bigint          | YES           |             0 | [Crew] External identifier for the course from external systems.                 |


### Foreign Keys

| FK_Name                   | Table_Name     | Column_Name   | Referenced_Table   | Referenced_Column   |
|:--------------------------|:---------------|:--------------|:-------------------|:--------------------|
| FK_Person_Courses_Persons | Person_Courses | PERSON_ID     | Persons            | PERSON_ID           |


---

## Lookup_Items

*User-defined lookup values and dropdown options used throughout the MXP system for data entry and display purposes*

### Columns

DEBUG: Table 'Lookup_Items' has 145 total columns, 65 have business definitions
DEBUG: After excluding columns: 61 columns remaining
DEBUG: Final result: 57 columns with business definitions
| COLUMN_NAME                | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:---------------------------|:----------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| ROW_COUNTER                | int             | NO            |             1 | [System] Primary key for the table.                                              |
| LOOKUP_ITEM_ID             | int             | YES           |             0 | [System] Unique identifier for a lookup item.                                    |
| LOOKUP_ITEM_NAME           | varchar(512)    | NO            |             0 | [System] Name of the lookup item used for display purposes.                      |
| LOOKUP_SUB_CATEGORY_ID     | int             | NO            |             0 | [System] ID of the sub-category this lookup item belongs to. FK to               |
|                            |                 |               |               | Lookup_Sub_Categories table.                                                     |
| DISPLAY_CODE               | varchar(20)     | YES           |             0 | [System] Short code used for display in dropdowns and forms.                     |
| LOOKUP_EXTRA_VARCHAR1      | varchar(1000)   | YES           |             0 | [System] Extra varchar field 1 for additional data storage.                      |
| LOOKUP_EXTRA_VARCHAR2      | varchar(1000)   | YES           |             0 | [System] Extra varchar field 2 for additional data storage.                      |
| LOOKUP_EXTRA_VARCHAR3      | varchar(1000)   | YES           |             0 | [System] Extra varchar field 3 for additional data storage.                      |
| LOOKUP_EXTRA_VARCHAR4      | varchar(1000)   | YES           |             0 | [System] Extra varchar field 4 for additional data storage.                      |
| LOOKUP_EXTRA_AMOUNT_1      | numeric         | YES           |             0 | [System] Extra amount field 1 for numeric data storage.                          |
| LOOKUP_EXTRA_AMOUNT_2      | numeric         | YES           |             0 | [System] Extra amount field 2 for numeric data storage.                          |
| LOOKUP_EXTRA_BOOLEAN1      | bit             | YES           |             0 | [System] Extra boolean field 1 for true/false data storage.                      |
| LOOKUP_EXTRA_BOOLEAN2      | bit             | YES           |             0 | [System] Extra boolean field 2 for true/false data storage.                      |
| SUPPLIED                   | bit             | NO            |             0 | [System] Whether this lookup item was supplied by the system. Values: 0 = User   |
|                            |                 |               |               | created, 1 = System supplied                                                     |
| ACTIVE                     | bit             | NO            |             0 | [System] Whether the lookup item is active. Values: 0 = Inactive, 1 = Active     |
| LOOKUP_TEXT_1              | text(2147483647 | YES           |             0 | [System] Extra text field 1 for large text data storage.                         |
|                            | )               |               |               |                                                                                  |
| LOOKUP_TEXT_2              | text(2147483647 | YES           |             0 | [System] Extra text field 2 for large text data storage.                         |
|                            | )               |               |               |                                                                                  |
| LOOKUP_IMAGE               | image(214748364 | YES           |             0 | [System] Binary data of the lookup item image.                                   |
|                            | 7)              |               |               |                                                                                  |
| LOOKUP_IMAGE_NAME          | varchar(40)     | YES           |             0 | [System] Name of the lookup item image file.                                     |
| LOOKUP_IMAGE_TYPE          | varchar(20)     | YES           |             0 | [System] Type/format of the lookup item image.                                   |
| LOOKUP_EXTRA_CHAR_1        | char(30)        | YES           |             0 | [System] Extra char field 1 for fixed-length character data.                     |
| LOOKUP_EXTRA_CHAR_2        | char(30)        | YES           |             0 | [System] Extra char field 2 for fixed-length character data.                     |
| REC_DELETED                | bit             | NO            |             0 | [System] Whether the lookup item record is deleted. Values: 0 = Not deleted, 1 = |
|                            |                 |               |               | Deleted                                                                          |
| CREATED_BY_ID              | int             | YES           |             0 | [System] ID of the user who created the lookup item. FK to MXP Users table.      |
| CREATED_AT_ID              | int             | YES           |             0 | [System] ID of the MXP instance where the lookup item was created. Values: 1 =   |
|                            |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                    |
| CREATED                    | datetime        | NO            |             0 | [System] Date and time when the lookup item was created.                         |
| LAST_CHANGED               | datetime        | NO            |             0 | [System] Date and time when the lookup item was last modified.                   |
| CHANGED                    | char(1)         | NO            |             0 | [System] Indicates if the record needs replication. Values: N = No, Y = Yes      |
| GUID                       | uniqueidentifie | YES           |             0 | [System] Unique identifier used for system integration and tracking. Should be   |
|                            | r               |               |               | returned in lowercase format.                                                    |
| LOOKUP_EXTRA_INTEGER1      | int             | YES           |             0 | [System] Extra integer field 1 for numeric data storage.                         |
| LOOKUP_EXTRA_INTEGER2      | int             | YES           |             0 | [System] Extra integer field 2 for numeric data storage.                         |
| ORG_UNIT_ID                | int             | YES           |             0 | [System] ID of the organizational unit where this lookup item is applicable. FK  |
|                            |                 |               |               | to Org_Units table.                                                              |
| LOOKUP_EXTRA_INTEGER3      | int             | YES           |             0 | [System] Extra integer field 3 for numeric data storage.                         |
| LOOKUP_EXTRA_INTEGER4      | int             | YES           |             0 | [System] Extra integer field 4 for numeric data storage.                         |
| LOOKUP_EXTRA_INTEGER5      | int             | YES           |             0 | [System] Extra integer field 5 for numeric data storage.                         |
| LOOKUP_EXTRA_INTEGER6      | int             | YES           |             0 | [System] Extra integer field 6 for numeric data storage.                         |
| LOOKUP_EXTRA_INTEGER7      | int             | YES           |             0 | [System] Extra integer field 7 for numeric data storage.                         |
| LOOKUP_EXTRA_DATE1         | datetime        | YES           |             0 | [System] Extra date field 1 for date data storage.                               |
| LOOKUP_EXTRA_DATE2         | datetime        | YES           |             0 | [System] Extra date field 2 for date data storage.                               |
| LOOKUP_ITEM_PARENT_ID      | int             | YES           |             0 | [System] ID of the parent lookup item for hierarchical relationships.            |
| LOOKUP_TEXT_3              | text(2147483647 | YES           |             0 | [System] Extra text field 3 for large text data storage.                         |
|                            | )               |               |               |                                                                                  |
| LOOKUP_EXTRA_BOOLEAN3      | bit             | YES           |             0 | [System] Extra boolean field 3 for true/false data storage.                      |
| LOOKUP_ITEM_NAME_ENGLISH   | varchar(512)    | YES           |             0 | [System] English translation of the lookup item name.                            |
| LOOKUP_ITEM_NAME_SPANISH   | varchar(512)    | YES           |             0 | [System] Spanish translation of the lookup item name.                            |
| LOOKUP_ITEM_NAME_FRENCH    | varchar(512)    | YES           |             0 | [System] French translation of the lookup item name.                             |
| LOOKUP_ITEM_NAME_GERMAN    | varchar(512)    | YES           |             0 | [System] German translation of the lookup item name.                             |
| LOOKUP_ITEM_NAME_ITALIAN   | varchar(512)    | YES           |             0 | [System] Italian translation of the lookup item name.                            |
| LOOKUP_ITEM_NAME_PORTUGESE | varchar(512)    | YES           |             0 | [System] Portuguese translation of the lookup item name.                         |
| LAST_CHANGE_LOG_ID         | bigint          | YES           |             0 | [System] ID of the last change tracking record for this lookup item.             |
| LOOKUP_EXTRA_INTEGER8      | int             | YES           |             0 | [System] Extra integer field 8 for numeric data storage.                         |
| LOOKUP_EXTRA_INTEGER9      | int             | YES           |             0 | [System] Extra integer field 9 for numeric data storage.                         |
| LOOKUP_EXTRA_AMOUNT_3      | numeric         | YES           |             0 | [System] Extra amount field 3 for numeric data storage.                          |
| LOOKUP_EXTRA_AMOUNT_4      | numeric         | YES           |             0 | [System] Extra amount field 4 for numeric data storage.                          |
| LOOKUP_EXTRA_AMOUNT_5      | numeric         | YES           |             0 | [System] Extra amount field 5 for numeric data storage.                          |
| LOOKUP_EXTRA_AMOUNT_6      | numeric         | YES           |             0 | [System] Extra amount field 6 for numeric data storage.                          |
| LOOKUP_EXTRA_BOOLEAN4      | bit             | YES           |             0 | [System] Extra boolean field 4 for true/false data storage.                      |
| LOOKUP_EXTRA_BOOLEAN5      | bit             | YES           |             0 | [System] Extra boolean field 5 for true/false data storage.                      |


### Foreign Keys

| FK_Name                               | Table_Name   | Column_Name            | Referenced_Table      | Referenced_Column      |
|:--------------------------------------|:-------------|:-----------------------|:----------------------|:-----------------------|
| FK_Lookup_Items_Lookup_Sub_Categories | Lookup_Items | LOOKUP_SUB_CATEGORY_ID | Lookup_Sub_Categories | LOOKUP_SUB_CATEGORY_ID |


---

## Sys_Lookup_Items

*System-defined lookup values and configuration data used for system operations and user interface elements*

### Columns

DEBUG: Table 'Sys_Lookup_Items' has 68 total columns, 54 have business definitions
DEBUG: After excluding columns: 46 columns remaining
DEBUG: Final result: 46 columns with business definitions
| COLUMN_NAME                    | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                            |
|:-------------------------------|:----------------|:--------------|--------------:|:-------------------------------------------------------------------------------|
| SYS_LOOKUP_ITEMS_ID            | int             | NO            |             1 | [System] Primary key for the table.                                            |
| SYS_LOOKUP_CATEGORY_ID         | int             | NO            |             0 | [System] ID of the system lookup category. FK to Sys_Lookup_Categories table.  |
| SYS_LOOKUP_ID                  | int             | NO            |             0 | [System] ID of the system lookup this item belongs to.                         |
| SYS_LOOKUP_ITEM_NAME           | varchar(100)    | NO            |             0 | [System] Name of the system lookup item used for display purposes.             |
| SYS_LOOKUP_DISPLAY_CODE        | varchar(50)     | YES           |             0 | [System] Short code used for display in system interfaces.                     |
| SYS_LOOKUP_CATEGORY            | int             | YES           |             0 | [System] Category number for the system lookup item.                           |
| SYS_LOOKUP_NUMBER1             | numeric         | NO            |             0 | [System] System lookup number field 1 for numeric data storage.                |
| SYS_LOOKUP_NUMBER2             | numeric         | NO            |             0 | [System] System lookup number field 2 for numeric data storage.                |
| SYS_LOOKUP_ACTIVE              | bit             | NO            |             0 | [System] Whether the system lookup item is active. Values: 0 = Inactive, 1 =   |
|                                |                 |               |               | Active                                                                         |
| REC_DELETED                    | bit             | NO            |             0 | [System] Whether the system lookup item record is deleted. Values: 0 = Not     |
|                                |                 |               |               | deleted, 1 = Deleted                                                           |
| CREATED_AT_ID                  | int             | YES           |             0 | [System] ID of the MXP instance where the system lookup item was created.      |
|                                |                 |               |               | Values: 1 = Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL      |
| CREATED                        | datetime        | NO            |             0 | [System] Date and time when the system lookup item was created.                |
| LAST_CHANGED                   | datetime        | NO            |             0 | [System] Date and time when the system lookup item was last modified.          |
| CHANGED                        | char(1)         | NO            |             0 | [System] Indicates if the record needs replication. Values: N = No, Y = Yes    |
| GUID                           | uniqueidentifie | YES           |             0 | [System] Unique identifier used for system integration and tracking. Should be |
|                                | r               |               |               | returned in lowercase format.                                                  |
| CREATED_BY_ID                  | int             | YES           |             0 | [System] ID of the user who created the system lookup item. FK to MXP Users    |
|                                |                 |               |               | table.                                                                         |
| SYS_LOOKUPS                    | varchar(500)    | YES           |             0 | [System] System lookup values or configuration data.                           |
| SYS_LOOKUP_DESCRIPTION         | text(2147483647 | YES           |             0 | [System] Detailed description of the system lookup item.                       |
|                                | )               |               |               |                                                                                |
| SYS_LOOKUP_FIELD_TYPE          | varchar(20)     | YES           |             0 | [System] Type of field this system lookup item represents.                     |
| SYS_LOOKUP_DOCUMENT            | image(214748364 | YES           |             0 | [System] Binary data of the system lookup document.                            |
|                                | 7)              |               |               |                                                                                |
| SYS_LOOKUP_INTEGER1            | int             | YES           |             0 | [System] System lookup integer field 1 for numeric data storage.               |
| SYS_LOOKUP_INTEGER2            | int             | YES           |             0 | [System] System lookup integer field 2 for numeric data storage.               |
| SYS_LOOKUP_BOOLEAN1            | bit             | YES           |             0 | [System] System lookup boolean field 1 for true/false data storage.            |
| SYS_LOOKUP_BOOLEAN2            | bit             | YES           |             0 | [System] System lookup boolean field 2 for true/false data storage.            |
| SYS_LOOKUP_DESCRIPTION2        | text(2147483647 | YES           |             0 | [System] Additional description field 2 for the system lookup item.            |
|                                | )               |               |               |                                                                                |
| SYS_LOOKUP_DESCRIPTION3        | text(2147483647 | YES           |             0 | [System] Additional description field 3 for the system lookup item.            |
|                                | )               |               |               |                                                                                |
| SYS_LOOKUP_DESCRIPTION4        | text(2147483647 | YES           |             0 | [System] Additional description field 4 for the system lookup item.            |
|                                | )               |               |               |                                                                                |
| SYS_LOOKUP_DESCRIPTION5        | text(2147483647 | YES           |             0 | [System] Additional description field 5 for the system lookup item.            |
|                                | )               |               |               |                                                                                |
| SYS_LOOKUP_DESCRIPTION6        | text(2147483647 | YES           |             0 | [System] Additional description field 6 for the system lookup item.            |
|                                | )               |               |               |                                                                                |
| SYS_LOOKUP_DATE1               | datetime        | YES           |             0 | [System] System lookup date field 1 for date data storage.                     |
| SYS_LOOKUP_DATE2               | datetime        | YES           |             0 | [System] System lookup date field 2 for date data storage.                     |
| LAST_CHANGE_LOG_ID             | bigint          | YES           |             0 | [System] ID of the last change tracking record for this system lookup item.    |
| SYS_LOOKUP_ITEM_ALIAS_NAME     | varchar(100)    | YES           |             0 | [System] Alias name for the system lookup item.                                |
| SYS_LOOKUP_ITEM_NAME_ENGLISH   | varchar(512)    | YES           |             0 | [System] English translation of the system lookup item name.                   |
| SYS_LOOKUP_ITEM_NAME_SPANISH   | varchar(512)    | YES           |             0 | [System] Spanish translation of the system lookup item name.                   |
| SYS_LOOKUP_ITEM_NAME_FRENCH    | varchar(512)    | YES           |             0 | [System] French translation of the system lookup item name.                    |
| SYS_LOOKUP_ITEM_NAME_GERMAN    | varchar(512)    | YES           |             0 | [System] German translation of the system lookup item name.                    |
| SYS_LOOKUP_ITEM_NAME_ITALIAN   | varchar(512)    | YES           |             0 | [System] Italian translation of the system lookup item name.                   |
| SYS_LOOKUP_ITEM_NAME_PORTUGESE | varchar(512)    | YES           |             0 | [System] Portuguese translation of the system lookup item name.                |
| SYS_LOOKUP_VARCHAR1            | varchar(50)     | YES           |             0 | [System] System lookup varchar field 1 for character data storage.             |
| SYS_LOOKUP_VARCHAR2            | varchar(50)     | YES           |             0 | [System] System lookup varchar field 2 for character data storage.             |
| SYS_LOOKUP_VARCHAR3            | varchar(50)     | YES           |             0 | [System] System lookup varchar field 3 for character data storage.             |
| SYS_LOOKUP_VARCHAR4            | varchar(50)     | YES           |             0 | [System] System lookup varchar field 4 for character data storage.             |
| SYS_LOOKUP_ITEM_ALIAS_CODE     | varchar(50)     | YES           |             0 | [System] Alias code for the system lookup item.                                |
| SYS_LOOKUP_IMAGE_1             | image(214748364 | YES           |             0 | [System] System lookup image field 1 for binary image data storage.            |
|                                | 7)              |               |               |                                                                                |
| SYS_LOOKUP_IMAGE_2             | image(214748364 | YES           |             0 | [System] System lookup image field 2 for binary image data storage.            |
|                                | 7)              |               |               |                                                                                |


### Foreign Keys

| FK_Name                                   | Table_Name       | Column_Name            | Referenced_Table      | Referenced_Column      |
|:------------------------------------------|:-----------------|:-----------------------|:----------------------|:-----------------------|
| FK_Sys_Lookup_Items_Sys_Lookup_Categories | Sys_Lookup_Items | SYS_LOOKUP_CATEGORY_ID | Sys_Lookup_Categories | SYS_LOOKUP_CATEGORY_ID |


---

## Interface_Queue_Log

*Monitors the MXP Kafka Consumer and Producer. Records incoming transactions from Kafka topics (direction=0) and outgoing messages from MXP Kafka Producer (direction=1). Tracks message processing, errors, and retry attempts for both consumer and producer operations.*

### Columns

DEBUG: Table 'Interface_Queue_Log' has 17 total columns, 17 have business definitions
DEBUG: Final result: 17 columns with business definitions
| COLUMN_NAME   | DATA_TYPE    | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                              |
|:--------------|:-------------|:--------------|--------------:|:---------------------------------------------------------------------------------|
| id            | bigint       | NO            |             1 | [System] Primary key for the interface queue log.                                |
| direction     | bit          | NO            |             0 | [System] Direction of the message. Values: 0 = Incoming (Consumer), 1 = Outgoing |
|               |              |               |               | (Producer)                                                                       |
| topic         | varchar(255) | NO            |             0 | [System] Kafka topic name for the message.                                       |
| groupId       | varchar(255) | YES           |             0 | [System] Kafka consumer group ID.                                                |
| msgKey        | varchar(255) | YES           |             0 | [System] Message key for Kafka partitioning.                                     |
| payload       | varchar(-1)  | NO            |             0 | [System] Message payload data.                                                   |
| partition     | int          | YES           |             0 | [System] Kafka partition number.                                                 |
| offset        | bigint       | YES           |             0 | [System] Kafka message offset.                                                   |
| created       | datetime     | NO            |             0 | [System] Date and time when the message was created.                             |
| processed     | datetime     | YES           |             0 | [System] Date and time when the message was processed.                           |
| errorCode     | int          | YES           |             0 | [System] Error code if processing failed.                                        |
| errorMsg      | varchar(-1)  | YES           |             0 | [System] Error message if processing failed.                                     |
| mrc           | int          | YES           |             0 | [System] Message retry count.                                                    |
| nextRetry     | datetime     | YES           |             0 | [System] Date and time for next retry attempt.                                   |
| processing    | bit          | YES           |             0 | [System] Whether the message is currently being processed.                       |
| execTime      | int          | YES           |             0 | [System] Execution time in milliseconds.                                         |
| warningMsg    | varchar(-1)  | YES           |             0 | [System] Warning message if any issues occurred.                                 |


### Foreign Keys

*No foreign keys found for this table.*

---

## Interface_Push_Notification_Log

*Queue table for outgoing messages processed by the MXP Kafka Producer. Contains items queued for outgoing messages where the Producer calls appropriate stored procedures to generate payloads and produces messages on respective topics. Also tracks internal interfaces (like Medical system) that don't use Kafka. INTERFACE_KAFKA timestamp indicates when Kafka message was produced - can be set to NULL to reprocess or populated with timestamp to skip processing.*

### Columns

DEBUG: Table 'Interface_Push_Notification_Log' has 27 total columns, 15 have business definitions
DEBUG: After excluding columns: 15 columns remaining
DEBUG: Final result: 15 columns with business definitions
| COLUMN_NAME       | DATA_TYPE       | IS_NULLABLE   |   IS_IDENTITY | BUSINESS_DEFINITION                                                             |
|:------------------|:----------------|:--------------|--------------:|:--------------------------------------------------------------------------------|
| ROW_COUNTER       | bigint          | NO            |             1 | [System] Primary key for the table.                                             |
| NOTIFICATION_TYPE | varchar(25)     | YES           |             0 | [System] Type of notification being sent.                                       |
| PERSON_ID         | int             | YES           |             0 | [System] ID of the person receiving the notification. FK to Persons table.      |
| ACCOUNT_ID        | int             | YES           |             0 | [System] ID of the account associated with the notification. FK to              |
|                   |                 |               |               | Person_Account table.                                                           |
| BOOKING_ID        | int             | YES           |             0 | [System] ID of the booking associated with the notification. FK to              |
|                   |                 |               |               | Person_Booking table.                                                           |
| NOTIFICATION_DATA | nvarchar(500)   | YES           |             0 | [System] Data payload for the notification.                                     |
| CREATED_AT_ID     | int             | YES           |             0 | [System] ID of the MXP instance where the notification was created. Values: 1 = |
|                   |                 |               |               | Head Office, 2 = SCL, 3 = Shipyard, 4 = VAL, 5 = RES, 6 = BRL                   |
| CREATED_BY_ID     | int             | YES           |             0 | [System] ID of the user who created the notification. FK to MXP Users table.    |
| CREATED           | datetime        | NO            |             0 | [System] Date and time when the notification record was created.                |
| LAST_CHANGED      | datetime        | NO            |             0 | [System] Date and time when the notification record was last modified.          |
| CHANGED           | char(1)         | NO            |             0 | [System] Indicates if the record needs replication. Values: N = No, Y = Yes     |
| GUID              | uniqueidentifie | NO            |             0 | [System] Unique identifier used for system integration and tracking. Should be  |
|                   | r               |               |               | returned in lowercase format.                                                   |
| INTERFACE_KAFKA   | datetime        | YES           |             0 | [System] Timestamp when Kafka message was produced. Set to NULL to reprocess    |
|                   |                 |               |               | message in next batch, or populate with timestamp to skip processing.           |
| CHANGED_FIELDS    | varchar(500)    | YES           |             0 | [System] List of fields that were changed in the notification.                  |
| INTERFACE_MEDICAL | datetime        | YES           |             0 | [System] Date and time when notification was sent via medical interface.        |


### Foreign Keys

*No foreign keys found for this table.*

---

