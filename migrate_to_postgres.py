#!/usr/bin/env python3
"""Copy question-bank content from the local SQLite database into PostgreSQL."""
import os
import getpass
import sqlite3
import sys
from pathlib import Path

import psycopg


def main():
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if not database_url:
        database_url = getpass.getpass("Supabase PostgreSQL connection string (input hidden): ").strip()
    if not database_url:
        raise SystemExit("A PostgreSQL connection string is required.")
    os.environ["DATABASE_URL"] = database_url
    from server import init_db

    source = Path(sys.argv[1] if len(sys.argv) > 1 else "learning_site.sqlite3")
    if not source.is_file():
        raise SystemExit(f"SQLite database not found: {source}")

    init_db()
    sqlite = sqlite3.connect(source)
    sqlite.row_factory = sqlite3.Row
    with psycopg.connect(database_url) as pg:
        with pg.cursor() as cur:
            questions = sqlite.execute("SELECT id,part,topic,question,created_at,created_by,translation,answer_structure FROM questions ORDER BY id").fetchall()
            cur.executemany(
                "INSERT INTO questions(id,part,topic,question,created_at,created_by,translation,answer_structure) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(id) DO UPDATE SET part=EXCLUDED.part,topic=EXCLUDED.topic,question=EXCLUDED.question,created_at=EXCLUDED.created_at,created_by=EXCLUDED.created_by,translation=EXCLUDED.translation,answer_structure=EXCLUDED.answer_structure",
                [(row["id"], row["part"], row["topic"], row["question"], row["created_at"], None, row["translation"], row["answer_structure"]) for row in questions],
            )
            cur.execute("SELECT setval(pg_get_serial_sequence('questions', 'id'), COALESCE((SELECT MAX(id) FROM questions), 1), EXISTS(SELECT 1 FROM questions))")
        pg.commit()
    sqlite.close()
    print(f"Migrated {len(questions)} questions. Local account credentials and progress were left in SQLite.")


if __name__ == "__main__":
    main()
