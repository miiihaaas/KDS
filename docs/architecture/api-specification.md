# API Specification

## REST API Overview

KDS sistem koristi RESTful API dizajn sa jasno definisanim endpoint-ima za sve entitete. API podržava JSON format za komunikaciju i implementira standardne HTTP status kodove.

## Authentication API

```yaml
/auth/login:
  post:
    summary: User authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
    responses:
      200:
        description: Successful login
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                user:
                  $ref: '#/components/schemas/User'
      401:
        description: Invalid credentials

/auth/logout:
  post:
    summary: User logout
    responses:
      200:
        description: Successful logout
```

## Client Management API

```yaml
/api/clients:
  get:
    summary: Get all clients
    parameters:
      - name: search
        in: query
        schema:
          type: string
      - name: tip
        in: query
        schema:
          type: string
          enum: [pravno_lice, fizicko_lice]
    responses:
      200:
        description: List of clients
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Client'
  
  post:
    summary: Create new client
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Client'
    responses:
      201:
        description: Client created
      400:
        description: Validation error

/api/clients/{id}:
  get:
    summary: Get client by ID
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Client details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Client'
      404:
        description: Client not found
```

## Device Management API

```yaml
/api/devices:
  get:
    summary: Get devices
    parameters:
      - name: room_id
        in: query
        schema:
          type: integer
      - name: tip
        in: query
        schema:
          type: string
    responses:
      200:
        description: List of devices

/api/devices/{id}/qr:
  get:
    summary: Get QR code for device
    responses:
      200:
        description: QR code image
        content:
          image/png:
            schema:
              type: string
              format: binary

/api/qr/scan:
  post:
    summary: Process scanned QR code
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              qr_data:
                type: string
    responses:
      200:
        description: Device information
        content:
          application/json:
            schema:
              type: object
              properties:
                device:
                  $ref: '#/components/schemas/Device'
                breadcrumb:
                  type: array
                  items:
                    type: object
```

## Work Order API

```yaml
/api/work-orders:
  get:
    summary: Get work orders
    parameters:
      - name: status
        in: query
        schema:
          type: string
      - name: serviser_id
        in: query
        schema:
          type: integer
      - name: date_from
        in: query
        schema:
          type: string
          format: date
      - name: date_to
        in: query
        schema:
          type: string
          format: date
    responses:
      200:
        description: List of work orders

  post:
    summary: Create new work order
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/WorkOrder'
    responses:
      201:
        description: Work order created

/api/work-orders/{id}/email:
  post:
    summary: Send work order via email
    responses:
      200:
        description: Email sent successfully
      500:
        description: Email sending failed
```
