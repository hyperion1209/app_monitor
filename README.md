# Web Ap Monitor Documentation

## Modules
### app_config.py
Contains the code for validating and loading the configuration file

### logger.py
Contains the code for creating the logger used in the project

### monitor.py
Contains the code for probing the endpoints, logging errors and sending notifications.

#### Properties
- runs a serial loop to probe the endpoints
- uses requests
- implements retries based on HTTP Status Codes
- 5xx errors are retried and logged as errors when retries are exhausted

### async_monitor.py
Contains the asyncio code for probing the endpoints, logging errors and sending notifications.

#### Properties
- runs an asyncio event loop
- uses httpx
- implements retries based on Connection Errors and Timeouts
- 5xx errors are not retried and logged as errors
