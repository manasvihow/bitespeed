# Bitespeed Identity Reconciliation Service

This project is a backend web service built to solve the Bitespeed identity reconciliation challenge. It provides an API endpoint that intelligently identifies and consolidates customer contact information, linking multiple email addresses and phone numbers to a single, primary identity.

---

## Live API Documentation (Swagger UI)

The service is hosted on Render. The interactive API documentation, powered by Swagger UI, is the best place to view and test the endpoint live from your browser.

**[https://manasvi-bitespeed-assignment.onrender.com/docs](https://manasvi-bitespeed-assignment.onrender.com/docs)**

---

## Tech Stack

* **Language**: Python 3
* **Framework**: FastAPI
* **Database ORM**: SQLModel
* **Production Database**: PostgreSQL (on Render)
* **Development Database**: SQLite
* **Deployment Platform**: Render

---

## API Endpoint Details

There is a single endpoint available to handle identity reconciliation.

### Identify Contact

This endpoint is used to identify a user, create new contacts, and link different contact details to a single identity.

* **Endpoint**: `/identify`
* **Method**: **`POST`**
* **URL**: `https://manasvi-bitespeed-assignment.onrender.com/identify`

#### Request Body

The request body must be a JSON object containing either an `email`, a `phoneNumber`, or both.

```json
{
  "email": "chris.evans@marvel.com",
  "phoneNumber": "1234"
}
```

#### Successfull Response (200 OK)

A successful request will return a consolidated contact view, showing the primary contact's ID along with a collection of all associated emails, phone numbers, and the IDs of any secondary contacts.

```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["chris.evans@marvel.com"],
    "phoneNumbers": ["1234"],
    "secondaryContactIds": []
  }
}
```
<details>
  <summary>Extending the previous example</summary>

   #### Request Body

   ```json
    {
        "email": "captain.america@avengers.com",
        "phoneNumber": "1234" /* Same number as Chris Evans */ 
    }
   ```

   #### Successful Response (200 OK)

   ```json
    {
        "contact":{
            "primaryContatctId": 1,
            "emails": ["chris.evans@marvel.com","captain.america@avengers.com"],
            "phoneNumbers": ["1234"],
            "secondaryContactIds": [2]
        }
    }
   ```
</details>
<details>
  <summary>In fact, all of the following requests will return the above response</summary>
  
   ```json
    {
	    "email": "",
	    "phoneNumber":"1234"
    }
   ```
   ```json
    {
	    "email": "chris.evans@marvel.com",
	    "phoneNumber":""
    }
   ```
   ```json
    {
	    "email": "captain.america@avengers.com",
	    "phoneNumber":""
    }
   ```
</details>

<details>
  <summary>When primary contacts turn into secondary contacts</summary>

  #### Request
  ```json
  {
    "email": "robert.downey@marvel.com",
    "phoneNumber": "4321"
  }
  ```
  ```json
  {
    "email": "iron.man@avengers.com", 
    "phoneNumber": "7777" /* Different number from Robert Downey */
  }
  ```

  #### Existing State of the Database

  | id  | phoneNumber | email                      | linkedId | linkPrecedence | createdAt                  | updatedAt                  | deletedAt |
  |-----|-------------|----------------------------|----------|----------------|----------------------------|----------------------------|-----------|
  | 1  | 1234      | chris.evans@marvel.com      | null     | primary        | 2025-07-17 00:00:00.374+00 | 2025-07-17 00:00:00.374+00 | null      |
  | 2  | 1234      | captain.america@avengers.com  | 1     | secondary        | 2025-07-17 05:30:00.11+00  | 2025-07-17 05:30:00.11+00  | null      |
  | 3  | 4321      | robert.downey@marvel.com | null     | primary        | 2025-07-17 05:45:00.11+00  | 2025-07-17 05:45:00.11+00  | null      |
  | 4  | 7777      | iron.man@avengers.com | null     | primary        | 2025-07-17 05:50:00.11+00  | 2025-07-17 05:50:00.11+00  | null      |

 #### Request Body
 
 ```json
  {
    "email": "iron.man@avengers.com",
    "phoneNumber": "4321"
  }
 ```
 ###### Note: This request has email and phone number of two different existing contacts

 #### Successful Response (200 OK)

 ```json
 {
	"contact":{
			"primaryContatctId": 3,
			"emails": ["robert.downey@marvel.com","iron.man@avengers.com"],
			"phoneNumbers": ["4321","7777"],
			"secondaryContactIds": [4]
		}
 }
 ```

 #### Updated State of the Database

  | id  | phoneNumber | email                      | linkedId | linkPrecedence | createdAt                  | updatedAt                  | deletedAt |
  |-----|-------------|----------------------------|----------|----------------|----------------------------|----------------------------|-----------|
  | 1  | 1234      | chris.evans@marvel.com      | null     | primary        | 2025-07-17 00:00:00.374+00 | 2025-07-17 00:00:00.374+00 | null      |
  | 2  | 1234      | captain.america@avengers.com  | 1     | secondary        | 2025-07-17 05:30:00.11+00  | 2025-07-17 05:30:00.11+00  | null      |
  | 3  | 4321      | robert.downey@marvel.com | null     | primary        | 2025-07-17 05:45:00.11+00  | 2025-07-17 05:45:00.11+00  | null      |
  | 4  | 7777      | iron.man@avengers.com | 3    | secondary        | 2025-07-17 05:50:00.11+00  | 2025-07-17 05:50:00.11+00  | null      |

</details>

## How to Run Locally

To set up and run this project on your local machine, follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/manasvihow/bitespeed>
    cd <bitespeed>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate # `source venv/Scripts/activate` for Windows
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the development server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`. The local environment uses a `database.db` SQLite file for storage, which will be created automatically. The interactive API documentation can be accessed locally at `http://127.0.0.1:8000/docs`.

## Author

####  Manasvi Bathula : [**GitHub**](https://github.com/manasvihow) | [**LinkedIn**](https://www.linkedin.com/in/manasvi-bathula/) | [**E-mail**](mailto:manasvi.bathula@gmail.com)