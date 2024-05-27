from enum import Enum


class OrderStatus(Enum):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class UserRole(Enum):
    ADMIN = "Admin"
    BUYER = "Buyer"
