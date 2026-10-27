ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'professor';

CREATE TABLE guardian_student_links (
  guardian_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (guardian_id, student_id)
);
CREATE INDEX idx_guardian_links_student ON guardian_student_links(student_id);

CREATE TABLE guardian_invites (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  code_hash TEXT NOT NULL UNIQUE,
  expires_at TEXT NOT NULL,
  used_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_guardian_invites_lookup ON guardian_invites(code_hash, expires_at, used_at);

CREATE TABLE homework (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  activity_id INTEGER REFERENCES activities(id) ON DELETE SET NULL,
  assigned_by INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  title TEXT NOT NULL,
  instructions TEXT NOT NULL,
  due_date TEXT,
  status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente','concluida')),
  completed_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_homework_student_status ON homework(student_id, status, created_at DESC);
