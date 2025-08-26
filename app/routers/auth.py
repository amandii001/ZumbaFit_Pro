from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth_schema import UserRegister, UserLogin, AdminLogin, UserResponse, AdminResponse
from app.db import get_connection, close_connection
from app.utils.hashing import hash_password, verify_password
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister):
    """Register a new user"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password and insert user
        hashed_pw = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (user.name, user.email, hashed_pw)
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        
        return UserResponse(
            user_id=user_id,
            name=user.name,
            email=user.email,
            message="✅ User registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.post("/login", response_model=UserResponse)
def login_user(user: UserLogin):
    """Login user"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Find user by email
        cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
        db_user = cursor.fetchone()
        
        if not db_user or not verify_password(user.password, db_user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Update last active timestamp
        cursor.execute(
            "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = %s",
            (db_user["user_id"],)
        )
        conn.commit()
        
        return UserResponse(
            user_id=db_user["user_id"],
            name=db_user["name"],
            email=db_user["email"],
            message="✅ Login successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.post("/admin/login", response_model=AdminResponse)
def login_admin(admin: AdminLogin):
    """Login admin"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Find admin by username or email
        if admin.username:
            cursor.execute("SELECT * FROM admin WHERE username=%s", (admin.username,))
        elif admin.email:
            cursor.execute("SELECT * FROM admin WHERE email=%s", (admin.email,))
        else:
            raise HTTPException(status_code=400, detail="Username or email is required")
        
        db_admin = cursor.fetchone()
        
        if not db_admin or not verify_password(admin.password, db_admin["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Update last login timestamp
        cursor.execute(
            "UPDATE admin SET last_login = CURRENT_TIMESTAMP WHERE admin_id = %s",
            (db_admin["admin_id"],)
        )
        conn.commit()
        
        return AdminResponse(
            admin_id=db_admin["admin_id"],
            username=db_admin["username"],
            role=db_admin["role"],
            message="✅ Admin login successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Admin login failed: {str(e)}")
    finally:
        close_connection(conn, cursor)
