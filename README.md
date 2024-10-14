<h1>Weather Email Notification Project</h1>

This project is a Python-based application that fetches weather data for a specific location (in this case, UCF - University of Central Florida) and sends a daily email with weather updates to a specified recipient. It utilizes the Open-Meteo API for weather data and Gmail's SMTP server to send the email.

<h2>Features</h2>
<ul>
    <li><b>Weather Fetching</b>: Retrieves the current and forecasted weather data (temperature, wind speed, wind direction, weather conditions) for specified times of the day (12 PM, 3 PM, 5 PM, 10 PM).</li>
    <li><b>Automatic Email Notifications</b>: Sends daily weather updates via email using Gmail's SMTP server.</li>
    <li><b>Customizable Time and Location</b>: Although the current project is set to send emails every day at 10 AM for UCF's location, the location and time can easily be adjusted.</li>
    <li><b>Configurable Email Information</b>: Email credentials and recipients are read from external files (emailInfo.txt and recipient.txt).</li>
</ul>

<h2>Technologies Used</h2>
<ul>
    <li><b>Python 3</b></li>
    <li><b>Open-Meteo API</b>: To fetch weather data.</li>
    <li><b>SMTP</b> (Simple Mail Transfer Protocol): To send text notifications through Gmail.</li>
    <li><b>JSON</b>: For parsing and handling API responses.</li>
</ul>

<h2>Project Structure</h2>
<pre>
src/
├── emailInfo.txt  # Contains email login information
├── recipient.txt  # Contains the email recipients
weather_email.py    # Main Python script
</pre>

<em>emailInfo.txt</em>

This file contains the credentials for the sender's email in the format:

<pre>
your-email@gmail.com
your-email-password
</pre>

<em>recipient.txt</em>

This file contains the phone numbers of the recipient(s).

How It Works
<ol>
    <li><b>Fetching Weather Data</b>: The application uses the Open-Meteo API to fetch weather data for a specific location (latitude and longitude). It retrieves both the current weather and hourly forecast data for specific times of the day.</li>
    <li><b>Parsing the Data</b>: The weather data is parsed and formatted into a human-readable string, showing the temperature in both Fahrenheit and Celsius, wind speed, wind direction, and a description of the weather conditions based on predefined codes.</li>
    <li><b>Sending the Email</b>: Using Gmail's SMTP server, the application logs into the sender's account (credentials stored in emailInfo.txt), formats the weather information, and sends the weather update to the recipient (phone number stored in recipient.txt).</li>
    <li><b>Daily Scheduling</b>: The application calculates the delay in seconds from the current time until 10 AM the next day. It runs in an infinite loop and sends the weather update every 24 hours at 10 AM.</li>
</ol>

Key Functions
<ul>
    <li><code>convertCelsiusToFahrenheit(temp: float) -> float</code>: Converts temperature from Celsius to Fahrenheit.</li>
    <li><code>getJSONInfo(longitude: float, latitude: float) -> dict</code>: Sends an HTTP GET request to the Open-Meteo API to fetch weather data for the given coordinates (longitude and latitude).</li>
    <li><code>parseJSON(json: dict) -> str</code>: Parses the JSON response from the API and formats it into a string with the relevant weather information for the current time, 12 PM, 3 PM, 5 PM, and 10 PM.</li>
    <li><code>validateInfo() -> list</code>: Reads the email credentials and recipient's email address from the files emailInfo.txt and recipient.txt.</li>
    <li><code>sendMessage(user: str, password: str, recipient: str, header: str, msg: str)</code>: Sends the email with the weather data using Gmail's SMTP server.</li>
    <li><code>getSecondDelay() -> float</code>: Calculates the delay in seconds until 10 AM the next day.</li>
    <li><code>main()</code>: The main function that ties everything together, calling all other functions to send the daily weather update.</li>
</ul>

<h2>Usage</h2>
<h3>Prerequisites</h3>
<ol>
    <li>Python 3: Ensure that Python 3 is installed on your system.</li>
    <li>Gmail Account: You need a Gmail account to send emails. Make sure to enable "Less secure apps" in your Gmail account settings if you encounter any issues with sending emails.</li>
</ol>

<h3>Setup</h3>
<ol>
    <li>Clone the repository or download the script.</li>
    <li>Create two text files in the src/ folder:</li>
      <ul>
        <li><b>emailInfo.txt</b>: Contains your Gmail email address and password on separate lines.</li>
        <li><b>recipient.txt</b>: Contains the recipient's phone number.</li>
      </ul>
    <li>
      Install necessary Python modules if they aren't already installed:
      <pre>pip install smtplib</pre>
    </li>
    <li>
      Run the script:
      <pre>python weather_email.py</pre>
    </li>
</ol>

The script will then run indefinitely, sending a daily weather update at 10 AM for the location (latitude 28.6024, longitude -81.2001, corresponding to UCF).
Customization
<ul>
    <li><b>Change Location</b>: Update the ucfLongitude and ucfLatitude values in the main() function to the desired location's coordinates.</li>
    <li><b>Change Notification Time</b>: Adjust the time of day in the getSecondDelay() function where the updated_date is set (currently, it's set to 10 AM daily).</li>
</ul>

<h2>Future Improvements</h2>
<ul>
    <li><b>Use a Proper Database</b>: Currently, email credentials and recipient information are stored in plain text files. In the future, this could be migrated to a secure database or environment variables.</li>
    <li><b>Error Handling</b>: Add more robust error handling for API failures or email delivery issues.</li>
    <li><b>Multiple Recipients</b>: Expand the functionality to support multiple recipients from a list.</li>
    <li><b>Logging</b>: Implement logging to keep track of when emails are sent and if any errors occur.</li>
</ul>
<h2>License</h2>

This project is open-source and available under the MIT License.

<em>This project provides a simple yet effective solution for daily weather notifications via email. By leveraging a free weather API and Python’s standard libraries, it can be easily customized and extended for more use cases.</em>
