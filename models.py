from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Databases.db import Base
from sqlalchemy.sql import func

# ==========================
# USERS
# ==========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    trust_score = Column(Float, default=100)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    phone_verified = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)

    # Relationships
    devices = relationship("Device", back_populates="user")
    logins = relationship("LoginHistory", back_populates="user")
    risk_events = relationship("RiskEvent", back_populates="user")
    verifications = relationship("VerificationLog", back_populates="user")
    otp_records = relationship("OTPRecord", back_populates="user")
    
    consent_given = Column(Boolean, default=False)
    consent_timestamp = Column(DateTime, nullable=True)
    data_retention_days = Column(Integer, default=365)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)


# ==========================
# DEVICES
# ==========================

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, unique=True, nullable=False, index=True)
    device_id = Column(String)
    device_name = Column(String)
    trusted = Column(Boolean, default=False)
    last_used = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="devices")


# ==========================
# LOGIN HISTORY
# ==========================

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String)
    location = Column(String)
    device_id = Column(String)
    risk_score = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="logins")


# ==========================
# RISK EVENTS
# ==========================

class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String)
    risk_score = Column(Float)
    decision = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="risk_events")


# ==========================
# VERIFICATION LOGS
# ==========================

class VerificationLog(Base):
    __tablename__ = "verification_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    face_match_score = Column(Float)
    liveness_passed = Column(Boolean)
    phone_verified = Column(Boolean)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="verifications")


# ==========================
# EMPLOYEES
# ==========================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)
    access_level = Column(Integer)

    activities = relationship("EmployeeActivity", back_populates="employee")


# ==========================
# EMPLOYEE ACTIVITIES
# ==========================

class EmployeeActivity(Base):
    __tablename__ = "employee_activity"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    action = Column(String)
    risk_score = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    employee = relationship("Employee", back_populates="activities")


# ==========================
# OTP RECORDS (MOVED OUTSIDE!)
# ==========================

class OTPRecord(Base):
    __tablename__ = "otp_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_code = Column(String(6), nullable=False)
    purpose = Column(String(50), nullable=False)  # "LOGIN", "TRANSACTION", "PASSWORD_RESET", etc.
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="otp_records")