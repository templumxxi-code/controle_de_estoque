from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class UserCreate(LoginRequest):
    full_name: str | None = Field(default=None, max_length=180)
    phone: str | None = Field(default=None, max_length=40)
    job_title: str | None = Field(default=None, max_length=120)
    role: str = Field(default="operator", pattern="^(admin|operator)$")
    must_change_password: bool = False


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=180)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    job_title: str | None = Field(default=None, max_length=120)
    role: str | None = Field(default=None, pattern="^(admin|operator)$")
    is_active: bool | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
    confirm_password: str


class PasswordReset(BaseModel):
    new_password: str = Field(min_length=8)


class ThemeUpdate(BaseModel):
    theme: str = Field(pattern="^(light|dark)$")


class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    full_name: str | None = None
    phone: str | None = None
    job_title: str | None = None
    role: str
    must_change_password: bool
    last_login_at: datetime | None
    theme_preference: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AuditLogOut(BaseModel):
    id: int
    user_id: int | None
    action: str
    entity: str | None
    entity_id: int | None
    description: str
    result: str
    ip_address: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CategoryOut(CategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(CategoryCreate):
    pass


class ProductCreate(BaseModel):
    internal_code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=2, max_length=180)
    category_id: int | None = None
    description: str | None = None
    unit: str = "un"
    minimum_stock: Decimal = Field(default=Decimal("0"), ge=0)
    purchase_cost: Decimal = Field(default=Decimal("0"), ge=0)
    sale_price: Decimal = Field(default=Decimal("0"), ge=0)
    desired_margin: Decimal = Field(default=Decimal("0"), ge=0, lt=1)
    brand: str | None = None
    model: str | None = None
    color: str | None = None
    size: str | None = None
    storage_location: str | None = None


class ProductOut(ProductCreate):
    id: int
    stock_quantity: Decimal
    is_active: bool
    created_at: datetime
    suggested_price: Decimal
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(ProductCreate):
    pass


class StockEntry(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)
    unit_cost: Decimal = Field(ge=0)
    reason: str | None = None
    document_number: str | None = None


class StockAdjustment(BaseModel):
    product_id: int
    adjustment_type: str = Field(pattern="^(increase|decrease|set)$")
    quantity: Decimal = Field(ge=0)
    reason: str = Field(min_length=3, max_length=500)


class StockMovementOut(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: Decimal
    previous_quantity: Decimal
    new_quantity: Decimal
    unit_cost: Decimal | None
    reason: str | None
    document_number: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal | None = Field(default=None, ge=0)


class SaleCreate(BaseModel):
    items: list[SaleItemCreate] = Field(min_length=1)
    payment_method: str = "pix"
    notes: str | None = None


class FinancialCreate(BaseModel):
    transaction_type: str = Field(pattern="^(income|expense)$")
    category: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0)
    payment_method: str = "pix"
    status: str = Field(default="paid", pattern="^(paid|pending)$")
    transaction_date: datetime | None = None
    notes: str | None = None


class FinancialUpdate(FinancialCreate):
    pass
