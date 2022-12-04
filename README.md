# IOTRegister
Register Service for an IOT project

## Register

**PATH**: /register

**METHOD**: POST

**PARAMETERS**:
- uid: str
- endpoint: str
- ...custom parameters...

**RESPONSE STATUS CODE**:
- 200: Item Registered or Updated
- 400: Generic Error

## Get

**PATH**: /item

**METHOD**: GET

**PARAMETERS**:
- uid: str

**RESPONSE STATUS CODE**:
- 200: No errors, read json response
- 400: Generic Error
- 404: Item not available

**RESPONSE**:
- uid: str
- endpoint: str
- online: bool
- ...custom parameters...

## Unregister

**PATH**: /unregister

**METHOD**: DELETE

**PARAMETERS**:
- uid: str

**RESPONSE STATUS CODE**:
- 200: Item unregistered
- 400: Generic Error

## Get Catalog

**PATH**: /catalog

**METHOD**: GET

**RESPONSE**: Array of JSONs
- uid: int
- endpoint: str
- online: bool
- ...custom parameters...
