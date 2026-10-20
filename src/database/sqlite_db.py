import sqlite3
import json
from pathlib import Path
from datetime import datetime
import bcrypt

DB_PATH = Path(__file__).resolve().parent.parent.parent / "attendance.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_sqlite_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        face_embedding TEXT,
        voice_embedding TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT NOT NULL,
        name TEXT NOT NULL,
        section TEXT NOT NULL,
        teacher_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        enrolled_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (subject_id, student_id),
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        is_present INTEGER NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    )
    """)
    conn.commit()

    # Seed demo teacher and subjects if database is fresh
    cursor.execute("SELECT COUNT(*) as count FROM teachers")
    if cursor.fetchone()["count"] == 0:
        hashed = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)",
            ("teacher", hashed, "Dr. Sarah Mitchell")
        )
        teacher_id = cursor.lastrowid

        # Seed subjects
        cursor.execute(
            "INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
            ("CS101", "AI & Machine Learning", "Section A", teacher_id)
        )
        sub1_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
            ("CS202", "Computer Vision & Robotics", "Section B", teacher_id)
        )
        sub2_id = cursor.lastrowid

        # Seed demo students
        students_seed = [
            ("Alex Johnson", None, None),
            ("Priya Sharma", None, None),
            ("David Lee", None, None),
            ("Emma Watson", None, None)
        ]
        s_ids = []
        for s_name, f_emb, v_emb in students_seed:
            cursor.execute(
                "INSERT INTO students (name, face_embedding, voice_embedding) VALUES (?, ?, ?)",
                (s_name, f_emb, v_emb)
            )
            s_ids.append(cursor.lastrowid)

        # Enroll students
        for sid in s_ids[:3]:
            cursor.execute(
                "INSERT OR IGNORE INTO subject_students (subject_id, student_id) VALUES (?, ?)",
                (sub1_id, sid)
            )
        for sid in s_ids[1:]:
            cursor.execute(
                "INSERT OR IGNORE INTO subject_students (subject_id, student_id) VALUES (?, ?)",
                (sub2_id, sid)
            )
        
        conn.commit()

    conn.close()


# Ensure tables are ready on module import
init_sqlite_db()


class SQLiteResponse:
    def __init__(self, data):
        self.data = data


class SQLiteTableQuery:
    def __init__(self, table_name):
        self.table_name = table_name
        self._select_fields = "*"
        self._where_clauses = []
        self._where_params = []
        self._action = "select"
        self._insert_data = None

    def select(self, fields="*"):
        self._select_fields = fields
        self._action = "select"
        return self

    def insert(self, data):
        self._action = "insert"
        self._insert_data = data
        return self

    def delete(self):
        self._action = "delete"
        return self

    def eq(self, column, value):
        self._where_clauses.append(f"{column} = ?")
        self._where_params.append(value)
        return self

    def execute(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            if self._action == "insert":
                items = self._insert_data if isinstance(self._insert_data, list) else [self._insert_data]
                inserted_rows = []
                for item in items:
                    cols = list(item.keys())
                    vals = []
                    for c in cols:
                        v = item[c]
                        if isinstance(v, bool):
                            v = 1 if v else 0
                        elif isinstance(v, (list, dict)):
                            v = json.dumps(v)
                        vals.append(v)
                    placeholders = ", ".join(["?"] * len(cols))
                    col_str = ", ".join(cols)
                    cursor.execute(
                        f"INSERT INTO {self.table_name} ({col_str}) VALUES ({placeholders})",
                        vals
                    )
                    row_id = cursor.lastrowid
                    cursor.execute(f"SELECT * FROM {self.table_name} WHERE rowid = ?", (row_id,))
                    row = cursor.fetchone()
                    inserted_rows.append(_row_to_dict(self.table_name, row))
                conn.commit()
                return SQLiteResponse(inserted_rows)

            elif self._action == "delete":
                where_str = f"WHERE {' AND '.join(self._where_clauses)}" if self._where_clauses else ""
                cursor.execute(f"DELETE FROM {self.table_name} {where_str}", self._where_params)
                conn.commit()
                return SQLiteResponse([])

            else:
                # Custom handler for complex joins used in Supabase syntax
                if self.table_name == "subject_students" and "students(*)" in self._select_fields:
                    where_str = f"WHERE {' AND '.join(self._where_clauses)}" if self._where_clauses else ""
                    query = f"""
                    SELECT ss.*, s.name as student_name, s.face_embedding, s.voice_embedding
                    FROM subject_students ss
                    JOIN students s ON ss.student_id = s.student_id
                    {where_str}
                    """
                    cursor.execute(query, self._where_params)
                    rows = cursor.fetchall()
                    result = []
                    for r in rows:
                        f_emb = json.loads(r["face_embedding"]) if r["face_embedding"] else None
                        v_emb = json.loads(r["voice_embedding"]) if r["voice_embedding"] else None
                        result.append({
                            "id": r["id"],
                            "subject_id": r["subject_id"],
                            "student_id": r["student_id"],
                            "enrolled_at": r["enrolled_at"],
                            "students": {
                                "student_id": r["student_id"],
                                "name": r["student_name"],
                                "face_embedding": f_emb,
                                "voice_embedding": v_emb
                            }
                        })
                    return SQLiteResponse(result)

                if self.table_name == "subject_students" and "subjects(*)" in self._select_fields:
                    where_str = f"WHERE {' AND '.join(self._where_clauses)}" if self._where_clauses else ""
                    query = f"""
                    SELECT ss.*, s.subject_code, s.name as sub_name, s.section, s.teacher_id
                    FROM subject_students ss
                    JOIN subjects s ON ss.subject_id = s.subject_id
                    {where_str}
                    """
                    cursor.execute(query, self._where_params)
                    rows = cursor.fetchall()
                    result = []
                    for r in rows:
                        result.append({
                            "id": r["id"],
                            "subject_id": r["subject_id"],
                            "student_id": r["student_id"],
                            "enrolled_at": r["enrolled_at"],
                            "subjects": {
                                "subject_id": r["subject_id"],
                                "subject_code": r["subject_code"],
                                "name": r["sub_name"],
                                "section": r["section"],
                                "teacher_id": r["teacher_id"]
                            }
                        })
                    return SQLiteResponse(result)

                if self.table_name == "attendance_logs" and "subjects(*)" in self._select_fields:
                    where_str = f"WHERE {' AND '.join(self._where_clauses)}" if self._where_clauses else ""
                    query = f"""
                    SELECT al.*, s.subject_code, s.name as sub_name, s.section, s.teacher_id
                    FROM attendance_logs al
                    JOIN subjects s ON al.subject_id = s.subject_id
                    {where_str}
                    """
                    cursor.execute(query, self._where_params)
                    rows = cursor.fetchall()
                    result = []
                    for r in rows:
                        result.append({
                            "id": r["id"],
                            "subject_id": r["subject_id"],
                            "student_id": r["student_id"],
                            "timestamp": r["timestamp"],
                            "is_present": bool(r["is_present"]),
                            "created_at": r["created_at"],
                            "subjects": {
                                "subject_id": r["subject_id"],
                                "subject_code": r["subject_code"],
                                "name": r["sub_name"],
                                "section": r["section"],
                                "teacher_id": r["teacher_id"]
                            }
                        })
                    return SQLiteResponse(result)

                if self.table_name == "attendance_logs" and "subjects!inner(*)" in self._select_fields:
                    # e.g. eq('subjects.teacher_id', teacher_id)
                    params = []
                    clauses = []
                    for c, v in zip(self._where_clauses, self._where_params):
                        col = c.replace("subjects.", "s.")
                        clauses.append(col)
                        params.append(v)
                    where_str = f"WHERE {' AND '.join(clauses)}" if clauses else ""
                    query = f"""
                    SELECT al.*, s.name as sub_name, s.subject_code, s.section, s.teacher_id
                    FROM attendance_logs al
                    JOIN subjects s ON al.subject_id = s.subject_id
                    {where_str}
                    """
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    result = []
                    for r in rows:
                        result.append({
                            "id": r["id"],
                            "subject_id": r["subject_id"],
                            "student_id": r["student_id"],
                            "timestamp": r["timestamp"],
                            "is_present": bool(r["is_present"]),
                            "created_at": r["created_at"],
                            "subjects": {
                                "subject_id": r["subject_id"],
                                "name": r["sub_name"],
                                "subject_code": r["subject_code"],
                                "section": r["section"],
                                "teacher_id": r["teacher_id"]
                            }
                        })
                    return SQLiteResponse(result)

                if self.table_name == "subjects":
                    where_str = f"WHERE {' AND '.join(self._where_clauses)}" if self._where_clauses else ""
                    cursor.execute(f"SELECT * FROM subjects {where_str}", self._where_params)
                    rows = cursor.fetchall()
                    result = []
                    for r in rows:
                        sub_dict = dict(r)
                        sub_id = sub_dict["subject_id"]
                        cursor.execute("SELECT COUNT(*) as cnt FROM subject_students WHERE subject_id = ?", (sub_id,))
                        cnt = cursor.fetchone()["cnt"]
                        sub_dict["subject_students"] = [{"count": cnt}]

                        cursor.execute("SELECT timestamp FROM attendance_logs WHERE subject_id = ?", (sub_id,))
                        att_rows = cursor.fetchall()
                        sub_dict["attendance_logs"] = [{"timestamp": a["timestamp"]} for a in att_rows]

                        result.append(sub_dict)
                    return SQLiteResponse(result)

                # Standard SELECT
                clean_select = self._select_fields.split("(")[0]
                if clean_select.strip() in ("*", ""):
                    cols_sql = "*"
                else:
                    cols_sql = self._select_fields

                where_str = f"WHERE {' AND '.join(self._where_clauses)}" if self._where_clauses else ""
                cursor.execute(f"SELECT {cols_sql} FROM {self.table_name} {where_str}", self._where_params)
                rows = cursor.fetchall()
                result = [_row_to_dict(self.table_name, r) for r in rows]
                return SQLiteResponse(result)

        finally:
            conn.close()


def _row_to_dict(table_name, row):
    if row is None:
        return None
    d = dict(row)
    if table_name == "students":
        if "face_embedding" in d and isinstance(d["face_embedding"], str):
            try:
                d["face_embedding"] = json.loads(d["face_embedding"])
            except Exception:
                pass
        if "voice_embedding" in d and isinstance(d["voice_embedding"], str):
            try:
                d["voice_embedding"] = json.loads(d["voice_embedding"])
            except Exception:
                pass
    if table_name == "attendance_logs":
        if "is_present" in d:
            d["is_present"] = bool(d["is_present"])
    return d


class SQLiteClient:
    def table(self, table_name):
        return SQLiteTableQuery(table_name)
