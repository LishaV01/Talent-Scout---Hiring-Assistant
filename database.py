"""
Database module for TalentScout Hiring Assistant
Handles all database operations for storing candidate data and responses
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import asdict
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manage all database operations"""
    
    def __init__(self, db_path: str = "talentscout.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create candidates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    full_name TEXT,
                    email TEXT,
                    phone TEXT,
                    years_experience INTEGER,
                    desired_positions TEXT,
                    current_location TEXT,
                    tech_stack TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create technical_questions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS technical_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    question_index INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
                )
            """)
            
            # Create technical_answers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS technical_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                    FOREIGN KEY (question_id) REFERENCES technical_questions (id)
                )
            """)
            
            # Create conversation_logs table for full conversation history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_session ON candidates(session_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_technical_questions_candidate ON technical_questions(candidate_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_technical_answers_candidate ON technical_answers(candidate_id)")
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def create_or_update_candidate(self, session_id: str, candidate_info) -> int:
        """Create or update candidate record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert lists to JSON strings
            desired_positions = json.dumps(candidate_info.desired_positions) if candidate_info.desired_positions else None
            tech_stack = json.dumps(candidate_info.tech_stack) if candidate_info.tech_stack else None
            
            # Check if candidate exists
            cursor.execute("SELECT id FROM candidates WHERE session_id = ?", (session_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute("""
                    UPDATE candidates 
                    SET full_name = ?, 
                        email = ?, 
                        phone = ?, 
                        years_experience = ?,
                        desired_positions = ?, 
                        current_location = ?, 
                        tech_stack = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """, (
                    candidate_info.full_name,
                    candidate_info.email,
                    candidate_info.phone,
                    candidate_info.years_experience,
                    desired_positions,
                    candidate_info.current_location,
                    tech_stack,
                    session_id
                ))
                candidate_id = existing[0]
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO candidates 
                    (session_id, full_name, email, phone, years_experience, 
                     desired_positions, current_location, tech_stack)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    candidate_info.full_name,
                    candidate_info.email,
                    candidate_info.phone,
                    candidate_info.years_experience,
                    desired_positions,
                    candidate_info.current_location,
                    tech_stack
                ))
                candidate_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            logger.info(f"Candidate {candidate_id} saved successfully")
            return candidate_id
            
        except Exception as e:
            logger.error(f"Error saving candidate: {e}")
            raise
    
    def save_technical_questions(self, candidate_id: int, questions: List[str]) -> List[int]:
        """Save technical questions for a candidate"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            question_ids = []
            for index, question in enumerate(questions):
                cursor.execute("""
                    INSERT INTO technical_questions 
                    (candidate_id, question_index, question)
                    VALUES (?, ?, ?)
                """, (candidate_id, index, question))
                question_ids.append(cursor.lastrowid)
            
            conn.commit()
            conn.close()
            logger.info(f"Saved {len(questions)} technical questions for candidate {candidate_id}")
            return question_ids
            
        except Exception as e:
            logger.error(f"Error saving technical questions: {e}")
            raise
    
    def save_technical_answer(self, candidate_id: int, question_index: int, answer: str) -> int:
        """Save a technical answer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get the question_id for this candidate and question_index
            cursor.execute("""
                SELECT id FROM technical_questions 
                WHERE candidate_id = ? AND question_index = ?
            """, (candidate_id, question_index))
            
            result = cursor.fetchone()
            if not result:
                logger.error(f"Question not found for candidate {candidate_id}, index {question_index}")
                return None
            
            question_id = result[0]
            
            # Save the answer
            cursor.execute("""
                INSERT INTO technical_answers 
                (candidate_id, question_id, answer)
                VALUES (?, ?, ?)
            """, (candidate_id, question_id, answer))
            
            answer_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Saved answer {answer_id} for question {question_id}")
            return answer_id
            
        except Exception as e:
            logger.error(f"Error saving technical answer: {e}")
            raise
    
    def save_conversation_log(self, candidate_id: int, role: str, content: str):
        """Save a conversation message"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversation_logs 
                (candidate_id, role, content)
                VALUES (?, ?, ?)
            """, (candidate_id, role, content))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving conversation log: {e}")
    
    def get_candidate_by_session(self, session_id: str) -> Optional[Dict]:
        """Get candidate data by session ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM candidates WHERE session_id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                data = dict(row)
                # Parse JSON fields
                if data.get('desired_positions'):
                    data['desired_positions'] = json.loads(data['desired_positions'])
                if data.get('tech_stack'):
                    data['tech_stack'] = json.loads(data['tech_stack'])
                return data
            return None
            
        except Exception as e:
            logger.error(f"Error getting candidate: {e}")
            return None
    
    def get_all_candidates(self, limit: int = 100) -> List[Dict]:
        """Get all candidates with basic info"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, full_name, email, phone, years_experience, 
                       current_location, created_at, updated_at
                FROM candidates 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting candidates: {e}")
            return []
    
    def get_candidate_full_data(self, candidate_id: int) -> Dict:
        """Get complete candidate data including questions and answers"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get candidate info
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
            candidate = cursor.fetchone()
            if not candidate:
                return None
            
            candidate_data = dict(candidate)
            
            # Parse JSON fields
            if candidate_data.get('desired_positions'):
                candidate_data['desired_positions'] = json.loads(candidate_data['desired_positions'])
            if candidate_data.get('tech_stack'):
                candidate_data['tech_stack'] = json.loads(candidate_data['tech_stack'])
            
            # Get technical Q&A
            cursor.execute("""
                SELECT tq.question, tq.question_index, ta.answer, ta.answered_at
                FROM technical_questions tq
                LEFT JOIN technical_answers ta ON tq.id = ta.question_id
                WHERE tq.candidate_id = ?
                ORDER BY tq.question_index
            """, (candidate_id,))
            
            qa_data = cursor.fetchall()
            candidate_data['technical_qa'] = [dict(row) for row in qa_data]
            
            # Get conversation logs
            cursor.execute("""
                SELECT role, content, timestamp
                FROM conversation_logs
                WHERE candidate_id = ?
                ORDER BY timestamp
            """, (candidate_id,))
            
            logs = cursor.fetchall()
            candidate_data['conversation_logs'] = [dict(row) for row in logs]
            
            conn.close()
            return candidate_data
            
        except Exception as e:
            logger.error(f"Error getting full candidate data: {e}")
            return None
    
    def export_to_json(self, output_file: str = "candidates_export.json"):
        """Export all data to JSON file"""
        try:
            candidates = self.get_all_candidates(limit=10000)
            full_data = []
            
            for candidate in candidates:
                candidate_data = self.get_candidate_full_data(candidate['id'])
                if candidate_data:
                    full_data.append(candidate_data)
            
            with open(output_file, 'w') as f:
                json.dump(full_data, f, indent=2, default=str)
            
            logger.info(f"Exported {len(full_data)} candidates to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False

# Helper function to generate session ID
def generate_session_id():
    """Generate unique session ID"""
    import uuid
    return str(uuid.uuid4())