# Component Methods

## Backend Component Methods

### AuthComponent

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `admin_login(store_id, username, password)` | str, str, str | JWT token | 관리자 로그인 |
| `admin_logout(token)` | str | bool | 관리자 로그아웃 |
| `table_login(store_id, table_number, password)` | str, int, str | JWT token | 테이블 로그인 |
| `verify_token(token)` | str | TokenPayload | JWT 토큰 검증 |
| `refresh_token(token)` | str | JWT token | 토큰 갱신 |
| `hash_password(password)` | str | str | bcrypt 해싱 |
| `check_login_attempts(identifier)` | str | bool | 로그인 시도 제한 확인 |

### MenuComponent

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `get_menus(store_id, category_id?)` | str, str? | List[Menu] | 메뉴 목록 조회 |
| `get_menu(menu_id)` | str | Menu | 메뉴 상세 조회 |
| `create_menu(store_id, menu_data)` | str, MenuCreate | Menu | 메뉴 생성 |
| `update_menu(menu_id, menu_data)` | str, MenuUpdate | Menu | 메뉴 수정 |
| `delete_menu(menu_id)` | str | bool | 메뉴 삭제 |
| `update_menu_order(menu_id, order)` | str, int | bool | 노출 순서 변경 |
| `upload_image(file)` | File | str (url) | 이미지 업로드 |
| `get_categories(store_id)` | str | List[Category] | 카테고리 목록 |
| `create_category(store_id, data)` | str, CategoryCreate | Category | 카테고리 생성 |
| `update_category(category_id, data)` | str, CategoryUpdate | Category | 카테고리 수정 |
| `delete_category(category_id)` | str | bool | 카테고리 삭제 |

### OrderComponent

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `create_order(session_id, items, tip_rate)` | str, List[OrderItem], int | Order | 주문 생성 |
| `get_orders(session_id)` | str | List[Order] | 세션별 주문 조회 |
| `get_order(order_id)` | str | Order | 주문 상세 조회 |
| `get_store_orders(store_id)` | str | List[Order] | 매장 전체 주문 |
| `update_order_status(order_id, status)` | str, str | Order | 주문 상태 변경 |
| `delete_order(order_id)` | str | bool | 주문 삭제 |
| `calculate_tip(subtotal, tip_rate)` | int, int | int | 팁 금액 계산 |
| `generate_order_number()` | - | str | 주문 번호 생성 |

### TableComponent

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `create_table(store_id, number, password)` | str, int, str | Table | 테이블 생성 |
| `get_tables(store_id)` | str | List[Table] | 테이블 목록 |
| `update_table(table_id, data)` | str, TableUpdate | Table | 테이블 수정 |
| `start_session(table_id)` | str | TableSession | 세션 시작 |
| `end_session(table_id)` | str | bool | 세션 종료 (이용 완료) |
| `get_table_history(table_id, date_from?, date_to?)` | str, date?, date? | List[OrderHistory] | 과거 내역 |
| `archive_session_orders(session_id)` | str | bool | 주문 이력 아카이빙 |

### WebSocketComponent

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `connect(store_id)` | str | Connection | WebSocket 연결 |
| `disconnect(connection_id)` | str | bool | 연결 해제 |
| `broadcast_new_order(store_id, order)` | str, Order | - | 신규 주문 브로드캐스트 |
| `broadcast_order_update(store_id, order)` | str, Order | - | 주문 상태 변경 브로드캐스트 |
| `broadcast_order_delete(store_id, order_id)` | str, str | - | 주문 삭제 브로드캐스트 |

---

**Note**: 상세 비즈니스 로직 (검증 규칙, 상태 전이 조건, 에러 처리 등)은 Functional Design 단계에서 정의됩니다.
