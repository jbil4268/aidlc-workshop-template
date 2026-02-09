# Backend API Summary

## API Endpoints

### Customer APIs

#### Authentication
- `POST /api/customer/auth/login` - Table login via QR code
- `POST /api/customer/auth/logout` - End table session

#### Menu
- `GET /api/customer/menu/list` - Get all categories and menus
- `GET /api/customer/menu/{menu_id}` - Get menu detail

#### Order
- `POST /api/customer/order/create` - Create new order
- `GET /api/customer/order/list` - Get all orders for session
- `GET /api/customer/order/{order_id}` - Get order detail

### Admin APIs

#### Authentication
- `POST /api/admin/auth/login` - Admin login with username/password

#### Order Management
- `GET /api/admin/order/list` - Get all orders (with optional status filter)
- `GET /api/admin/order/{order_id}` - Get order detail
- `PATCH /api/admin/order/{order_id}/status` - Update order status

#### Table Management
- `GET /api/admin/table/list` - Get all tables
- `GET /api/admin/table/{table_id}` - Get table detail
- `POST /api/admin/table/create` - Create new table
- `PATCH /api/admin/table/{table_id}` - Update table

#### Menu Management
- `GET /api/admin/menu/list` - Get all menus
- `GET /api/admin/menu/{menu_id}` - Get menu detail
- `POST /api/admin/menu/create` - Create new menu
- `PATCH /api/admin/menu/{menu_id}` - Update menu
- `POST /api/admin/menu/{menu_id}/upload-image` - Upload menu image
- `DELETE /api/admin/menu/{menu_id}` - Delete menu (soft delete)

#### Category Management
- `GET /api/admin/category/list` - Get all categories
- `GET /api/admin/category/{category_id}` - Get category detail
- `POST /api/admin/category/create` - Create new category
- `PATCH /api/admin/category/{category_id}` - Update category
- `DELETE /api/admin/category/{category_id}` - Delete category

### WebSocket
- `WS /ws/admin/{store_id}` - Real-time order updates for admin

## Authentication

### Customer Authentication
- Uses session tokens generated at table login
- Session token passed in request body or query parameter

### Admin Authentication
- Uses JWT tokens
- Token passed in `Authorization` header as `Bearer <token>`
- Token expires after 8 hours (configurable)

## Error Handling

All errors return JSON response with `detail` field:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad Request (validation errors, business rule violations)
- `401` - Unauthorized (invalid/expired token)
- `404` - Not Found
- `500` - Internal Server Error

## Data Models

### Order Status Flow
```
pending -> preparing -> ready -> served
                    \-> cancelled
```

### Tip Rates
Allowed values: 0, 5, 10, 15, 20 (percentage)

### Order Number Format
`#001`, `#002`, ... (resets daily per store)

## WebSocket Messages

### Message Types

#### New Order
```json
{
  "type": "new_order",
  "data": {
    "id": 1,
    "order_number": "#001",
    "table_number": "T1",
    "status": "pending",
    ...
  }
}
```

#### Order Update
```json
{
  "type": "order_update",
  "data": {
    "id": 1,
    "status": "preparing",
    ...
  }
}
```

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
