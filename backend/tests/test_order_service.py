"""Tests for OrderService"""
import pytest
from datetime import date, datetime
from app.services.order_service import OrderService, OrderItemData
from app.models import Store, Table, TableSession, Category, Menu, Order
from app.utils.errors import (
    InvalidTipRateError, SessionNotActiveError, 
    MenuNotAvailableError, InvalidQuantityError,
    OrderNotFoundError, InvalidStatusError
)


class TestOrderService:
    """Test suite for OrderService"""

    def setup_method(self, db_session):
        """Setup test fixtures"""
        self.db = db_session
        self.service = OrderService(self.db)
        
        # Create test data
        store = Store(id=1, name="Test Store")
        self.db.add(store)
        
        table = Table(id=1, store_id=1, table_number="T1", qr_code="QR001", is_active=True)
        self.db.add(table)
        
        session = TableSession(id=1, table_id=1, session_token="token123", started_at=datetime.utcnow())
        self.db.add(session)
        
        category = Category(id=1, store_id=1, name="Main", display_order=0)
        self.db.add(category)
        
        menu = Menu(id=1, category_id=1, name="Burger", price=10000, is_available=True)
        self.db.add(menu)
        
        self.db.commit()

    # TC-backend-017: 첫 주문 번호
    def test_generate_order_number_first(self, db_session):
        """Test generating first order number of the day"""
        self.setup_method(db_session)
        
        order_number = self.service.generate_order_number(store_id=1, order_date=date.today())
        
        assert order_number == "#001"

    # TC-backend-018: 순차 번호
    def test_generate_order_number_sequential(self, db_session):
        """Test generating sequential order numbers"""
        self.setup_method(db_session)
        
        # Create first order
        order1 = Order(
            session_id=1,
            order_number="#001",
            subtotal_amount=10000,
            tip_rate=0,
            tip_amount=0,
            total_amount=10000,
            status="pending",
            created_at=datetime.utcnow()
        )
        self.db.add(order1)
        self.db.commit()
        
        # Generate next number
        order_number = self.service.generate_order_number(store_id=1, order_date=date.today())
        
        assert order_number == "#002"

    # TC-backend-019: 다른 날짜 리셋
    def test_generate_order_number_different_date(self, db_session):
        """Test order number resets on different date"""
        self.setup_method(db_session)
        
        from datetime import timedelta
        yesterday = date.today() - timedelta(days=1)
        
        # Create order from yesterday
        order1 = Order(
            session_id=1,
            order_number="#005",
            subtotal_amount=10000,
            tip_rate=0,
            tip_amount=0,
            total_amount=10000,
            status="pending",
            created_at=datetime(yesterday.year, yesterday.month, yesterday.day)
        )
        self.db.add(order1)
        self.db.commit()
        
        # Today's order should start from #001
        order_number = self.service.generate_order_number(store_id=1, order_date=date.today())
        
        assert order_number == "#001"

    # TC-backend-020: 팁 0%
    def test_calculate_tip_zero(self, db_session):
        """Test tip calculation with 0%"""
        self.setup_method(db_session)
        
        tip = self.service.calculate_tip(subtotal=10000, tip_rate=0)
        
        assert tip == 0

    # TC-backend-021: 팁 10%
    def test_calculate_tip_ten_percent(self, db_session):
        """Test tip calculation with 10%"""
        self.setup_method(db_session)
        
        tip = self.service.calculate_tip(subtotal=10000, tip_rate=10)
        
        assert tip == 1000

    # TC-backend-022: 팁 15% 반올림
    def test_calculate_tip_rounding(self, db_session):
        """Test tip calculation with rounding"""
        self.setup_method(db_session)
        
        # 10333 * 0.15 = 1549.95 -> rounds to 1550
        tip = self.service.calculate_tip(subtotal=10333, tip_rate=15)
        
        assert tip == 1550

    # TC-backend-023: 잘못된 팁 비율
    def test_calculate_tip_invalid_rate(self, db_session):
        """Test tip calculation with invalid rate"""
        self.setup_method(db_session)
        
        with pytest.raises(InvalidTipRateError):
            self.service.calculate_tip(subtotal=10000, tip_rate=25)

    # TC-backend-024: 주문 생성 성공
    def test_create_order_success(self, db_session):
        """Test successful order creation"""
        self.setup_method(db_session)
        
        items = [OrderItemData(menu_id=1, quantity=2)]
        order = self.service.create_order(session_id=1, items=items, tip_rate=10)
        
        assert order is not None
        assert order.session_id == 1
        assert order.subtotal_amount == 20000
        assert order.tip_rate == 10
        assert order.tip_amount == 2000
        assert order.total_amount == 22000
        assert len(order.items) == 1

    # TC-backend-025: 비활성 세션
    def test_create_order_inactive_session(self, db_session):
        """Test order creation with inactive session"""
        self.setup_method(db_session)
        
        # End the session
        session = self.db.query(TableSession).filter_by(id=1).first()
        session.ended_at = datetime.utcnow()
        self.db.commit()
        
        items = [OrderItemData(menu_id=1, quantity=1)]
        
        with pytest.raises(SessionNotActiveError):
            self.service.create_order(session_id=1, items=items, tip_rate=0)

    # TC-backend-026: 주문 불가능한 메뉴
    def test_create_order_unavailable_menu(self, db_session):
        """Test order creation with unavailable menu"""
        self.setup_method(db_session)
        
        # Make menu unavailable
        menu = self.db.query(Menu).filter_by(id=1).first()
        menu.is_available = False
        self.db.commit()
        
        items = [OrderItemData(menu_id=1, quantity=1)]
        
        with pytest.raises(MenuNotAvailableError):
            self.service.create_order(session_id=1, items=items, tip_rate=0)

    # TC-backend-027: 수량 0 이하
    def test_create_order_invalid_quantity(self, db_session):
        """Test order creation with invalid quantity"""
        self.setup_method(db_session)
        
        items = [OrderItemData(menu_id=1, quantity=0)]
        
        with pytest.raises(InvalidQuantityError):
            self.service.create_order(session_id=1, items=items, tip_rate=0)

    # TC-backend-028: 상태 변경 성공
    def test_update_order_status_success(self, db_session):
        """Test successful order status update"""
        self.setup_method(db_session)
        
        # Create order
        items = [OrderItemData(menu_id=1, quantity=1)]
        order = self.service.create_order(session_id=1, items=items, tip_rate=0)
        
        # Update status
        updated = self.service.update_order_status(order_id=order.id, new_status="preparing")
        
        assert updated.status.value == "preparing"

    # TC-backend-029: 존재하지 않는 주문
    def test_update_order_status_not_found(self, db_session):
        """Test updating non-existent order"""
        self.setup_method(db_session)
        
        with pytest.raises(OrderNotFoundError):
            self.service.update_order_status(order_id=999, new_status="preparing")

    # TC-backend-030: 잘못된 상태 값
    def test_update_order_status_invalid(self, db_session):
        """Test updating order with invalid status"""
        self.setup_method(db_session)
        
        # Create order
        items = [OrderItemData(menu_id=1, quantity=1)]
        order = self.service.create_order(session_id=1, items=items, tip_rate=0)
        
        with pytest.raises(InvalidStatusError):
            self.service.update_order_status(order_id=order.id, new_status="invalid_status")
