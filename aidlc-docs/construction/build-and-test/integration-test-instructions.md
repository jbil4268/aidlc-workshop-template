# Integration Test Instructions

## Overview

Integration tests verify interactions between units and components:
- Backend API endpoints (Unit 1)
- Customer Frontend ↔ Backend (Unit 2 ↔ Unit 1)
- Admin Frontend ↔ Backend (Unit 3 ↔ Unit 1)
- WebSocket real-time communication

---

## Prerequisites

### All Units Running
1. Backend API Server (http://localhost:8000)
2. Customer Frontend (http://localhost:5173)
3. Admin Frontend (http://localhost:5174)

### Test Tools
- **Manual Testing**: Browser-based
- **API Testing**: Postman, curl, or Python requests
- **Optional**: Playwright/Cypress for E2E automation

---

## Test Scenarios

### Scenario 1: Customer Order Flow (End-to-End)

**Purpose**: Verify complete customer journey from QR scan to order completion

**Steps**:

1. **Admin: Create Test Data**
   - Login to Admin Frontend (http://localhost:5174)
   - Create Category: "음료"
   - Create Menu: "아메리카노" (price: 4500, category: 음료)
   - Create Table: "Table 1" (capacity: 4)

2. **Customer: QR Scan & Login**
   - Open Customer Frontend (http://localhost:5173)
   - Click "QR 코드 스캔"
   - Scan QR code for Table 1 (or manually enter table_id)
   - Verify: Redirected to /menu page
   - Verify: SessionStorage has table_id and session_id

3. **Customer: Browse Menu**
   - Verify: Menu list displays "아메리카노"
   - Click menu item
   - Verify: Menu detail shows price, description
   - Click "장바구니에 추가"
   - Verify: Cart badge shows "1"

4. **Customer: Create Order**
   - Click cart icon
   - Verify: Cart shows "아메리카노 x1"
   - Select tip: 10%
   - Verify: Subtotal = 4500, Tip = 450, Total = 4950
   - Click "주문하기"
   - Verify: Success message
   - Verify: Redirected to /order-status

5. **Admin: Receive Order (Real-time)**
   - Check Admin Dashboard
   - Verify: New order appears in "대기중" section
   - Verify: Notification sound plays
   - Verify: Order shows Table 1, 아메리카노 x1, Total 4950

6. **Admin: Update Order Status**
   - Click order card
   - Change status to "준비중"
   - Verify: Order moves to "준비중" section

7. **Customer: Check Status (Polling)**
   - Check /order-status page
   - Verify: Status updated to "준비중" (within 5 seconds)

8. **Admin: Complete Order**
   - Change status to "완료"
   - Verify: Order moves to "완료" section

9. **Customer: Session End**
   - Click "세션 종료"
   - Verify: Redirected to /qr-scan
   - Verify: SessionStorage cleared

**Expected Results**:
- ✅ All steps complete without errors
- ✅ Real-time updates work (WebSocket)
- ✅ Order calculations correct
- ✅ Session management works

---

### Scenario 2: Multiple Orders (Concurrent)

**Purpose**: Test system behavior with multiple simultaneous orders

**Steps**:

1. **Setup**: Create 3 tables, 5 menu items
2. **Customer 1**: Login Table 1, order 2 items
3. **Customer 2**: Login Table 2, order 3 items
4. **Customer 3**: Login Table 3, order 1 item
5. **Admin**: Verify all 3 orders appear
6. **Admin**: Process orders in different order
7. **Customers**: Verify status updates independently

**Expected Results**:
- ✅ No order mixing between tables
- ✅ Each customer sees only their orders
- ✅ Admin sees all orders correctly
- ✅ Status updates don't interfere

---

### Scenario 3: Error Handling

**Purpose**: Verify error handling across units

#### Test 3.1: Invalid Table Login
1. Customer: Enter non-existent table_id
2. Verify: Error message "테이블을 찾을 수 없습니다"

#### Test 3.2: Duplicate Session
1. Customer 1: Login Table 1
2. Customer 2: Try to login Table 1
3. Verify: Error "이미 활성화된 세션이 있습니다"

#### Test 3.3: Order After Session End
1. Customer: Login, add items to cart
2. Admin: Manually end session (DB or API)
3. Customer: Try to create order
4. Verify: Error "세션이 종료되었습니다"

#### Test 3.4: Unavailable Menu
1. Admin: Set menu to unavailable
2. Customer: Try to order that menu
3. Verify: Error "품절된 메뉴입니다"

#### Test 3.5: Invalid Order Status
1. Admin: Try to change order status to invalid value
2. Verify: Error message or validation

**Expected Results**:
- ✅ All errors handled gracefully
- ✅ User-friendly error messages
- ✅ No system crashes

---

### Scenario 4: WebSocket Real-time Updates

**Purpose**: Verify WebSocket communication

**Steps**:

1. **Setup**: Open Admin Frontend in 2 browser tabs
2. **Customer**: Create new order
3. **Admin Tab 1**: Verify order appears
4. **Admin Tab 2**: Verify order appears
5. **Admin Tab 1**: Change order status
6. **Admin Tab 2**: Verify status updated
7. **Close Admin Tab 1**
8. **Customer**: Create another order
9. **Admin Tab 2**: Verify order appears

**Expected Results**:
- ✅ All connected clients receive updates
- ✅ Updates appear within 1 second
- ✅ No duplicate notifications
- ✅ Connection resilient to tab close/reopen

---

### Scenario 5: Data Persistence

**Purpose**: Verify data persists across restarts

**Steps**:

1. **Admin**: Create 2 tables, 3 menus, 1 category
2. **Customer**: Login, create order
3. **Stop Backend**: Ctrl+C on backend server
4. **Restart Backend**: `uvicorn app.main:app --reload`
5. **Admin**: Refresh page, login
6. **Verify**: All tables, menus, categories exist
7. **Verify**: Order still exists with correct status
8. **Customer**: Refresh page
9. **Verify**: Session still active (if not expired)

**Expected Results**:
- ✅ All data persists in SQLite
- ✅ No data loss on restart
- ✅ Sessions maintain state

---

## API Integration Tests (Optional)

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Test 1: Admin Login
response = requests.post(f"{BASE_URL}/admin/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
assert response.status_code == 200
token = response.json()["access_token"]

# Test 2: Create Table
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/admin/tables", 
    json={"table_number": "T1", "capacity": 4},
    headers=headers
)
assert response.status_code == 201
table_id = response.json()["id"]

# Test 3: Customer Login
response = requests.post(f"{BASE_URL}/customer/auth/login", 
    json={"table_id": table_id}
)
assert response.status_code == 200
session_token = response.json()["access_token"]

# Test 4: Get Menu
headers = {"Authorization": f"Bearer {session_token}"}
response = requests.get(f"{BASE_URL}/customer/menu", headers=headers)
assert response.status_code == 200
assert isinstance(response.json(), list)

# Test 5: Create Order
response = requests.post(f"{BASE_URL}/customer/orders",
    json={
        "items": [{"menu_id": 1, "quantity": 2}],
        "tip_rate": 10
    },
    headers=headers
)
assert response.status_code == 201
order_id = response.json()["id"]

print("All API integration tests passed!")
```

### Using curl

```bash
# Admin Login
curl -X POST http://localhost:8000/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Create Menu
curl -X POST http://localhost:8000/admin/menu \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"아메리카노","price":4500,"category_id":1}'

# Customer Login
curl -X POST http://localhost:8000/customer/auth/login \
  -H "Content-Type: application/json" \
  -d '{"table_id":1}'
```

---

## Performance Tests (Optional)

### Load Testing with Apache Bench

```bash
# Test menu list endpoint
ab -n 1000 -c 10 http://localhost:8000/customer/menu

# Expected: 
# - Requests per second: > 100
# - Average response time: < 100ms
```

### Concurrent Orders

```bash
# Simulate 10 concurrent orders
for i in {1..10}; do
  curl -X POST http://localhost:8000/customer/orders \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"items":[{"menu_id":1,"quantity":1}],"tip_rate":0}' &
done
wait
```

---

## Test Checklist

### Backend API (Unit 1)
- [ ] All endpoints return correct status codes
- [ ] Authentication works (JWT)
- [ ] Authorization prevents unauthorized access
- [ ] Database transactions work correctly
- [ ] Error responses include helpful messages
- [ ] CORS allows frontend origins

### Customer Frontend (Unit 2)
- [ ] QR scan redirects to menu
- [ ] Menu list displays correctly
- [ ] Cart management works
- [ ] Order creation succeeds
- [ ] Order status polling works
- [ ] Session management works
- [ ] Error messages display

### Admin Frontend (Unit 3)
- [ ] Login works
- [ ] Dashboard shows orders
- [ ] WebSocket updates work
- [ ] Order status changes work
- [ ] CRUD operations work (tables, menus, categories)
- [ ] Notification sound plays

### Cross-Unit Integration
- [ ] Customer orders appear in Admin
- [ ] Admin status changes reflect in Customer
- [ ] Multiple customers don't interfere
- [ ] Data persists across restarts
- [ ] WebSocket handles multiple clients

---

## Troubleshooting

### WebSocket Not Working
- Check browser console for connection errors
- Verify backend WebSocket endpoint: ws://localhost:8000/ws
- Check CORS settings in backend

### Orders Not Appearing
- Check backend logs for errors
- Verify database has order records: `sqlite3 table_order.db "SELECT * FROM orders;"`
- Check network tab for failed API calls

### Session Issues
- Clear browser SessionStorage
- Check backend session records: `SELECT * FROM table_sessions;`
- Verify JWT token not expired

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Complete
