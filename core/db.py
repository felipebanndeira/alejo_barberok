import psycopg2
import psycopg2.extras
from psycopg2 import pool
from flask import g
import os
from dotenv import load_dotenv

load_dotenv()

_pool = None

def get_pool():
    global _pool
    if _pool is None or _pool.closed:
        _pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=os.environ['DATABASE_URL'],
            cursor_factory=psycopg2.extras.DictCursor
        )
    return _pool


class _PgWrapper:
    """
    Wraps a psycopg2 connection to expose the same .execute() / .executemany() /
    .commit() / .close() interface that sqlite3 connections provide, so the rest
    of the app (routes/, core/availability.py) doesn't need to change its call sites.

    DictCursor is set at the connection level, so every cursor returns rows that
    support BOTH index access (row[0]) and name access (row['column']),
    matching sqlite3.Row behaviour.
    """

    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=None):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        return cur

    def executemany(self, sql, seq_of_params):
        cur = self._conn.cursor()
        cur.executemany(sql, seq_of_params)
        return cur

    def commit(self):
        try:
            self._conn.commit()
        except Exception:
            pass

    def close(self):
        # No cerramos el socket físico aquí, se retorna al pool en close_db()
        pass


def get_db():
    if 'db' not in g:
        p = get_pool()
        try:
            conn = p.getconn()
            if conn.closed:
                p.putconn(conn, close=True)
                conn = p.getconn()
        except Exception:
            global _pool
            _pool = None
            conn = get_pool().getconn()

        g.db = _PgWrapper(conn)
        g._raw_conn = conn
    return g.db


def close_db(e=None):
    raw_conn = g.pop('_raw_conn', None)
    g.pop('db', None)
    if raw_conn is not None and _pool is not None and not _pool.closed:
        try:
            if e:
                raw_conn.rollback()
            else:
                raw_conn.commit()
            get_pool().putconn(raw_conn)
        except Exception:
            try:
                get_pool().putconn(raw_conn, close=True)
            except Exception:
                pass


def init_db():
    db = get_db()

    db.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id       SERIAL PRIMARY KEY,
            name     TEXT    NOT NULL,
            price    INTEGER NOT NULL,
            duration INTEGER NOT NULL
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id             SERIAL PRIMARY KEY,
            client_name    TEXT    NOT NULL,
            client_phone   TEXT    NOT NULL,
            service_id     INTEGER REFERENCES services(id),
            date           TEXT    NOT NULL,
            time           TEXT    NOT NULL,
            status         TEXT    DEFAULT 'pending',
            payment_method TEXT    DEFAULT 'efectivo',
            confirmed_at   TIMESTAMPTZ
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            id          SERIAL PRIMARY KEY,
            type        TEXT NOT NULL,
            date        TEXT,
            day_of_week INTEGER,
            start_time  TEXT,
            end_time    TEXT
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id           SERIAL PRIMARY KEY,
            product_name TEXT    NOT NULL,
            price        INTEGER NOT NULL,
            created_at   TIMESTAMPTZ DEFAULT NOW()
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id         SERIAL PRIMARY KEY,
            concept    TEXT    NOT NULL,
            amount     INTEGER NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT        NOT NULL
        )
    ''')

    # Seed default services
    if db.execute('SELECT COUNT(*) FROM services').fetchone()[0] == 0:
        db.execute("INSERT INTO services (name, price, duration) VALUES (%s, %s, %s)", ('Corte', 10000, 30))
        db.execute("INSERT INTO services (name, price, duration) VALUES (%s, %s, %s)", ('Barba', 4000, 30))
        db.execute("INSERT INTO services (name, price, duration) VALUES (%s, %s, %s)", ('Corte y barba', 12000, 30))

    # Seed default settings
    if db.execute('SELECT COUNT(*) FROM settings').fetchone()[0] == 0:
        settings_data = [
            ('barber_name',          'Alejo Barber'),
            ('logo_path',            'logo.png'),
            ('whatsapp',             '123456789'),
            ('deposit_percentage',   '50'),
            ('bank_details',         'CBU: 0000000000000000000000\nAlias: alejo.barber'),
            ('hours_mon_fri_start_1','10:30'),
            ('hours_mon_fri_end_1',  '13:30'),
            ('hours_mon_fri_start_2','16:30'),
            ('hours_mon_fri_end_2',  '21:30'),
            ('hours_sat_start',      '09:00'),
            ('hours_sat_end',        '13:30'),
        ]
        db.executemany("INSERT INTO settings (key, value) VALUES (%s, %s)", settings_data)

    # Seed default admin user
    from werkzeug.security import generate_password_hash
    if db.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        db.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            ('admin', generate_password_hash('admin'))
        )

    db.commit()
