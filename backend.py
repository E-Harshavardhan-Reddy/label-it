"""
Enhanced backend service for LabelIt! - Professional grade with analytics
"""

import json
import os
import uuid
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sqlite3
from contextlib import contextmanager
import logging
import pandas as pd
import zipfile
import io
from collections import defaultdict

# Configure minimal logging for production
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """SQLite database manager with professional-grade features"""
    
    def __init__(self, db_path: str = "data/labelit.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with comprehensive schema"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with self.get_connection() as conn:
            # Enable optimizations
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            conn.execute("PRAGMA temp_store=memory")
            conn.execute("PRAGMA foreign_keys=ON")
            
            # Enhanced users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    preferred_language TEXT DEFAULT 'en',
                    full_name TEXT,
                    email TEXT,
                    age INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    profile_picture TEXT
                )
            """)
            
            # Enhanced images table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    uploaded_by TEXT NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    latitude REAL,
                    longitude REAL,
                    city TEXT,
                    country TEXT,
                    location_method TEXT,
                    file_size INTEGER,
                    image_width INTEGER,
                    image_height INTEGER,
                    is_verified BOOLEAN DEFAULT FALSE,
                    verification_score REAL DEFAULT 0.0,
                    view_count INTEGER DEFAULT 0,
                    label_count INTEGER DEFAULT 0,
                    FOREIGN KEY (uploaded_by) REFERENCES users (username) ON DELETE CASCADE
                )
            """)
            
            # Enhanced labels table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS labels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    language TEXT NOT NULL,
                    added_by TEXT NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_verified BOOLEAN DEFAULT FALSE,
                    confidence_score REAL DEFAULT 1.0,
                    verification_count INTEGER DEFAULT 0,
                    is_offensive BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE,
                    FOREIGN KEY (added_by) REFERENCES users (username) ON DELETE CASCADE,
                    UNIQUE(image_id, text, language)
                )
            """)
            
            # Analytics table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    user_id TEXT,
                    image_id TEXT,
                    label_id INTEGER,
                    metadata TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT
                )
            """)
            
            # User activities table for detailed tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT,
                    points_earned INTEGER DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (username) ON DELETE CASCADE
                )
            """)
            
            # Add missing columns safely
            self._add_missing_columns(conn)
            
            # Create indexes for performance
            self._create_indexes(conn)
            
            conn.commit()
    
    def _add_missing_columns(self, conn):
        """Add missing columns to existing tables"""
        columns_to_add = [
            ("users", "last_login", "TIMESTAMP"),
            ("users", "is_active", "BOOLEAN DEFAULT TRUE"),
            ("users", "profile_picture", "TEXT"),
            ("images", "is_verified", "BOOLEAN DEFAULT FALSE"),
            ("images", "verification_score", "REAL DEFAULT 0.0"),
            ("images", "view_count", "INTEGER DEFAULT 0"),
            ("images", "label_count", "INTEGER DEFAULT 0"),
            ("labels", "verification_count", "INTEGER DEFAULT 0"),
            ("labels", "is_offensive", "BOOLEAN DEFAULT FALSE"),
        ]
        
        for table, column, definition in columns_to_add:
            try:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            except sqlite3.OperationalError:
                pass  # Column already exists
    
    def _create_indexes(self, conn):
        """Create database indexes for optimal performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_language ON users(preferred_language)",
            "CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_images_uploaded_by ON images(uploaded_by)",
            "CREATE INDEX IF NOT EXISTS idx_images_category ON images(category)",
            "CREATE INDEX IF NOT EXISTS idx_images_uploaded_at ON images(uploaded_at)",
            "CREATE INDEX IF NOT EXISTS idx_images_location ON images(latitude, longitude)",
            "CREATE INDEX IF NOT EXISTS idx_images_verified ON images(is_verified)",
            "CREATE INDEX IF NOT EXISTS idx_labels_image_id ON labels(image_id)",
            "CREATE INDEX IF NOT EXISTS idx_labels_language ON labels(language)",
            "CREATE INDEX IF NOT EXISTS idx_labels_text ON labels(text)",
            "CREATE INDEX IF NOT EXISTS idx_labels_added_by ON labels(added_by)",
            "CREATE INDEX IF NOT EXISTS idx_labels_verified ON labels(is_verified)",
            "CREATE INDEX IF NOT EXISTS idx_analytics_event ON analytics(event_type)",
            "CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_analytics_user ON analytics(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_activities_user ON user_activities(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_activities_type ON user_activities(activity_type)",
        ]
        
        for index_sql in indexes:
            conn.execute(index_sql)
    
    @contextmanager
    def get_connection(self):
        """Get database connection with optimizations"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

class BackendService:
    """Professional backend service with comprehensive features"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def log_event(self, event_type: str, user_id: str = None, metadata: Dict = None):
        """Log events for analytics"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO analytics (event_type, user_id, metadata)
                    VALUES (?, ?, ?)
                """, (event_type, user_id, json.dumps(metadata) if metadata else None))
                conn.commit()
        except Exception as e:
            logger.error(f"Error logging event: {e}")
    
    def create_user(self, username: str, password: str, **kwargs) -> Tuple[bool, str]:
        """Create user with enhanced validation"""
        try:
            username = username.strip()
            password = password.strip()
            
            if not username or not password:
                return False, "Username and password are required"
            
            if len(username) < 3:
                return False, "Username must be at least 3 characters"
            
            if len(password) < 3:
                return False, "Password must be at least 3 characters"
            
            if not username.replace('_', '').replace('-', '').isalnum():
                return False, "Username can only contain letters, numbers, underscore, and hyphen"
            
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO users (
                        username, password, preferred_language, 
                        full_name, email, age, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    username, password,
                    kwargs.get('preferred_language', 'en'),
                    kwargs.get('full_name', '').strip() or None,
                    kwargs.get('email', '').strip() or None,
                    kwargs.get('age') if kwargs.get('age', 0) > 12 else None,
                    datetime.now()
                ))
                conn.commit()
                
                # Log user creation
                self.log_event('user_registered', username, {
                    'language': kwargs.get('preferred_language', 'en'),
                    'has_full_name': bool(kwargs.get('full_name')),
                    'has_email': bool(kwargs.get('email'))
                })
                
                return True, "User created successfully"
                
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False, f"Error creating user: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user and update last login"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id FROM users 
                    WHERE username = ? AND password = ? AND is_active = TRUE
                """, (username, password))
                
                user = cursor.fetchone()
                
                if user:
                    # Update last login
                    conn.execute("""
                        UPDATE users SET last_login = ? WHERE username = ?
                    """, (datetime.now(), username))
                    conn.commit()
                    
                    # Log successful login
                    self.log_event('user_login', username)
                    return True
                    
                return False
                
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return False
    
    def add_image(self, title: str, description: str, category: str, 
                  image_path: str, uploaded_by: str, **kwargs) -> str:
        """Add image with comprehensive metadata"""
        try:
            image_id = str(uuid.uuid4())
            
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO images (
                        id, title, description, category, image_path, uploaded_by,
                        latitude, longitude, city, country, location_method,
                        file_size, image_width, image_height, uploaded_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    image_id, title, description, category, image_path, uploaded_by,
                    kwargs.get('latitude'), kwargs.get('longitude'),
                    kwargs.get('city'), kwargs.get('country'),
                    kwargs.get('location_method'),
                    kwargs.get('file_size'), kwargs.get('image_width'),
                    kwargs.get('image_height'), datetime.now()
                ))
                conn.commit()
                
                # Log image upload
                self.log_event('image_uploaded', uploaded_by, {
                    'image_id': image_id,
                    'category': category,
                    'has_location': bool(kwargs.get('latitude')),
                    'file_size': kwargs.get('file_size')
                })
                
                # Record user activity
                self._record_user_activity(
                    uploaded_by, 'image_upload', 
                    f'Uploaded image: {title}', 10
                )
                
                return image_id
                
        except Exception as e:
            logger.error(f"Error adding image: {e}")
            raise
    
    def add_label(self, image_id: str, text: str, language: str, added_by: str) -> bool:
        """Add label with enhanced features"""
        try:
            with self.db.get_connection() as conn:
                # Add label
                conn.execute("""
                    INSERT OR REPLACE INTO labels (
                        image_id, text, language, added_by, added_at
                    ) VALUES (?, ?, ?, ?, ?)
                """, (image_id, text, language, added_by, datetime.now()))
                
                # Update image label count
                conn.execute("""
                    UPDATE images SET label_count = (
                        SELECT COUNT(*) FROM labels WHERE image_id = ?
                    ) WHERE id = ?
                """, (image_id, image_id))
                
                conn.commit()
                
                # Log label addition
                self.log_event('label_added', added_by, {
                    'image_id': image_id,
                    'language': language,
                    'text_length': len(text)
                })
                
                # Record user activity
                self._record_user_activity(
                    added_by, 'label_add',
                    f'Added label: {text[:50]}...', 5
                )
                
                return True
                
        except Exception as e:
            logger.error(f"Error adding label: {e}")
            return False
    
    def _record_user_activity(self, user_id: str, activity_type: str, 
                             description: str, points: int = 0):
        """Record user activity for gamification"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO user_activities (
                        user_id, activity_type, description, points_earned
                    ) VALUES (?, ?, ?, ?)
                """, (user_id, activity_type, description, points))
                conn.commit()
        except Exception as e:
            logger.error(f"Error recording user activity: {e}")
    
    def get_images(self, category=None, language=None, search=None, limit=50) -> List[Dict]:
        """Get images with advanced filtering"""
        try:
            with self.db.get_connection() as conn:
                query = """
                    SELECT DISTINCT i.*, 
                           COUNT(l.id) as total_labels,
                           GROUP_CONCAT(DISTINCT l.language) as languages
                    FROM images i
                    LEFT JOIN labels l ON i.id = l.image_id
                    WHERE 1=1
                """
                params = []
                
                if category:
                    query += " AND i.category = ?"
                    params.append(category)
                
                if language:
                    query += " AND l.language = ?"
                    params.append(language)
                
                if search:
                    query += " AND (i.title LIKE ? OR i.description LIKE ? OR l.text LIKE ?)"
                    search_param = f"%{search}%"
                    params.extend([search_param, search_param, search_param])
                
                query += """
                    GROUP BY i.id
                    ORDER BY i.uploaded_at DESC
                    LIMIT ?
                """
                params.append(limit)
                
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting images: {e}")
            return []
    
    def get_image_labels(self, image_id: str) -> List[Dict]:
        """Get labels for specific image"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM labels 
                    WHERE image_id = ? 
                    ORDER BY added_at DESC
                """, (image_id,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting image labels: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get comprehensive platform statistics"""
        try:
            with self.db.get_connection() as conn:
                stats = {}
                
                # Basic counts
                cursor = conn.execute("SELECT COUNT(*) FROM images")
                stats['total_images'] = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM labels")
                stats['total_labels'] = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
                stats['total_users'] = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(DISTINCT language) FROM labels")
                stats['languages_used'] = cursor.fetchone()[0]
                
                # Advanced metrics
                cursor = conn.execute("""
                    SELECT AVG(label_count) FROM images WHERE label_count > 0
                """)
                result = cursor.fetchone()
                stats['avg_labels_per_image'] = round(result[0] if result[0] else 0, 2)
                
                # Recent activity (last 7 days)
                week_ago = datetime.now() - timedelta(days=7)
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM images WHERE uploaded_at > ?
                """, (week_ago,))
                stats['recent_images'] = cursor.fetchone()[0]
                
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM labels WHERE added_at > ?
                """, (week_ago,))
                stats['recent_labels'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def get_user_stats(self, username: str) -> Dict:
        """Get user-specific statistics"""
        try:
            with self.db.get_connection() as conn:
                stats = {}
                
                # Images uploaded
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM images WHERE uploaded_by = ?
                """, (username,))
                stats['images_uploaded'] = cursor.fetchone()[0]
                
                # Labels added
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM labels WHERE added_by = ?
                """, (username,))
                stats['labels_added'] = cursor.fetchone()[0]
                
                # Languages contributed
                cursor = conn.execute("""
                    SELECT COUNT(DISTINCT language) FROM labels WHERE added_by = ?
                """, (username,))
                stats['languages_contributed'] = cursor.fetchone()[0]
                
                # Categories contributed
                cursor = conn.execute("""
                    SELECT COUNT(DISTINCT category) FROM images WHERE uploaded_by = ?
                """, (username,))
                stats['categories_contributed'] = cursor.fetchone()[0]
                
                # Total points earned
                cursor = conn.execute("""
                    SELECT COALESCE(SUM(points_earned), 0) FROM user_activities WHERE user_id = ?
                """, (username,))
                stats['total_points'] = cursor.fetchone()[0]
                
                # User rank
                cursor = conn.execute("""
                    SELECT COUNT(*) + 1 FROM (
                        SELECT user_id, SUM(points_earned) as total_points
                        FROM user_activities
                        GROUP BY user_id
                        HAVING total_points > (
                            SELECT COALESCE(SUM(points_earned), 0)
                            FROM user_activities WHERE user_id = ?
                        )
                    )
                """, (username,))
                stats['user_rank'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    def get_category_statistics(self) -> Dict:
        """Get category distribution statistics"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT category, COUNT(*) as count
                    FROM images
                    GROUP BY category
                    ORDER BY count DESC
                """)
                return dict(cursor.fetchall())
        except Exception as e:
            logger.error(f"Error getting category statistics: {e}")
            return {}
    
    def get_language_statistics(self) -> Dict:
        """Get language usage statistics"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT language, COUNT(*) as count
                    FROM labels
                    GROUP BY language
                    ORDER BY count DESC
                """)
                return dict(cursor.fetchall())
        except Exception as e:
            logger.error(f"Error getting language statistics: {e}")
            return {}
    
    def get_activity_timeline(self, days=30) -> List[Dict]:
        """Get activity timeline for charts"""
        try:
            with self.db.get_connection() as conn:
                start_date = datetime.now() - timedelta(days=days)
                cursor = conn.execute("""
                    SELECT DATE(uploaded_at) as date, COUNT(*) as uploads
                    FROM images
                    WHERE uploaded_at > ?
                    GROUP BY DATE(uploaded_at)
                    ORDER BY date
                """, (start_date,))
                return [{'date': row[0], 'uploads': row[1]} for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting activity timeline: {e}")
            return []
    
    def export_to_excel(self) -> bytes:
        """Export all data to Excel format"""
        try:
            with self.db.get_connection() as conn:
                # Create Excel writer
                output = io.BytesIO()
                
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Export users
                    users_df = pd.read_sql_query("""
                        SELECT username, preferred_language, full_name, email, 
                               created_at, last_login, is_active
                        FROM users
                    """, conn)
                    users_df.to_excel(writer, sheet_name='Users', index=False)
                    
                    # Export images
                    images_df = pd.read_sql_query("""
                        SELECT id, title, description, category, uploaded_by,
                               uploaded_at, latitude, longitude, city, country,
                               file_size, image_width, image_height, label_count
                        FROM images
                    """, conn)
                    images_df.to_excel(writer, sheet_name='Images', index=False)
                    
                    # Export labels
                    labels_df = pd.read_sql_query("""
                        SELECT l.*, i.title as image_title
                        FROM labels l
                        JOIN images i ON l.image_id = i.id
                    """, conn)
                    labels_df.to_excel(writer, sheet_name='Labels', index=False)
                    
                    # Export statistics
                    stats = self.get_statistics()
                    stats_df = pd.DataFrame([stats])
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                
                output.seek(0)
                return output.getvalue()
                
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            return None
    
    def create_images_zip(self) -> bytes:
        """Create ZIP archive of all images"""
        try:
            output = io.BytesIO()
            
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                with self.db.get_connection() as conn:
                    cursor = conn.execute("""
                        SELECT id, title, category, image_path, uploaded_by
                        FROM images
                        WHERE image_path IS NOT NULL
                    """)
                    
                    for image in cursor.fetchall():
                        if os.path.exists(image['image_path']):
                            # Create organized folder structure
                            folder_name = f"{image['category']}/{image['uploaded_by']}"
                            file_extension = os.path.splitext(image['image_path'])[1]
                            archive_path = f"{folder_name}/{image['title'][:50]}{file_extension}"
                            
                            zip_file.write(image['image_path'], archive_path)
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating images ZIP: {e}")
            return None

# Global backend instance
backend = BackendService()
