# Smart Farm Irrigation System

## Running the MQTT and HTTP Server

1. Ensure you have Node.js installed.
2. Navigate to the directory containing `server.js`.
3. Install the required packages and run the server:

    ```sh
    npm install mosca express body-parser
    node server.js
    ```

## Running the Scheduler Manager

1. Ensure you have Python and the necessary packages installed.
2. Navigate to the directory containing `SchedulerManager.py`.
3. Install the required packages and run the script:

    ```sh
    pip install minimalmodbus paho-mqtt
    python SchedulerManager.py
    ```
