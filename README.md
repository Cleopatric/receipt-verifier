# Introduction
Service with simple authentication  for receipt validating in [App Store](https://developer.apple.com/documentation/appstorereceipts/verifyreceipt).

# Endpoints
- Sign up in service
    ```http
    POST http://0.0.0.0:8080/api/sign_up
    ```
-  Getting user info and receipts - `session authentication required`.
    ```http
    GET http://0.0.0.0:8080/api/get_user_receipts
    ```
- Verify receipt - `session authentication required`.
    ```http
    POST http://0.0.0.0:8080/api/verify_receipt
    ```
    

# Configure and run application
1.  Clone git repository:
    ```sh
    git clone https://github.com/Cleopatric/receipt-verifier.git
    ```

2.  Open repository
    ```sh
    cd  receipt-verifier
    ```

3.  Set virtual environment variables in **.env** file:
    ```sh
    # .env file
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    ```

4.  Run project (for this you need [Docker](https://docs.docker.com/compose/install/))
    
    Run services in the background:
    ```sh
    docker-compose up -d
    ```
    
    Run services in the foreground:
    ```sh
    docker-compose up --build
    ```
    
    Bring services down:
    ```sh
    docker-compose down
    ```
    
# Running tests
1.  Open repository
    ```sh
    cd  receipt-verifier
    ```
    
2. Set virtual environment:
    ```sh
    python3 -m venv venv
    ```

3. Activate virtual environment:
    
    MacOS/Linux
    
    ```sh
    source venv/bin/activate
    ```
    
    Windows
    ```sh
    venv\Scripts\activate
    ```
4. Install requirements:
    ```sh
      pip install -r requirements.txt
    ```
    
5. Open tests repository:
    ```sh
     cd server/tests/
    ```

6. Run tests:
    ```sh
    pytest tests
    ```
