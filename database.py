import sqlite3
import json
import os
from datetime import datetime

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect('court_scraper.db')
    cursor = conn.cursor()
    
    # Create queries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            case_number TEXT NOT NULL,
            filing_year TEXT NOT NULL,
            query_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            error_message TEXT
        )
    ''')
    
    # Create responses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id INTEGER,
            sno TEXT,
            case_no TEXT,
            case_no_link TEXT,
            date TEXT,
            date_link TEXT,
            party TEXT,
            corrigendum TEXT,
            pdf_filename TEXT,
            raw_response TEXT,
            response_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (query_id) REFERENCES queries (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def log_query(case_type, case_number, filing_year):
    """Log a new query to the database"""
    conn = sqlite3.connect('court_scraper.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO queries (case_type, case_number, filing_year)
        VALUES (?, ?, ?)
    ''', (case_type, case_number, filing_year))
    
    query_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return query_id

def update_query_status(query_id, status, error_message=None):
    """Update the status of a query"""
    conn = sqlite3.connect('court_scraper.db')
    cursor = conn.cursor()
    
    if error_message:
        cursor.execute('''
            UPDATE queries 
            SET status = ?, error_message = ?
            WHERE id = ?
        ''', (status, error_message, query_id))
    else:
        cursor.execute('''
            UPDATE queries 
            SET status = ?
            WHERE id = ?
        ''', (status, query_id))
    
    conn.commit()
    conn.close()

def log_response(query_id, result_data, raw_response=None):
    """Log the response data to the database"""
    conn = sqlite3.connect('court_scraper.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO responses (
            query_id, sno, case_no, case_no_link, date, date_link, 
            party, corrigendum, pdf_filename, raw_response
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        query_id,
        result_data.get('sno'),
        result_data.get('case_no'),
        result_data.get('case_no_link'),
        result_data.get('date'),
        result_data.get('date_link'),
        result_data.get('party'),
        result_data.get('corrigendum'),
        result_data.get('pdf'),
        raw_response
    ))
    
    conn.commit()
    conn.close()

def get_query_history(limit=10):
    """Get recent query history"""
    conn = sqlite3.connect('court_scraper.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT q.case_type, q.case_number, q.filing_year, q.status, 
               q.query_timestamp, r.case_no, r.party
        FROM queries q
        LEFT JOIN responses r ON q.id = r.query_id
        ORDER BY q.query_timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_query_stats():
    """Get statistics about queries"""
    conn = sqlite3.connect('court_scraper.db')
    cursor = conn.cursor()
    
    # Total queries
    cursor.execute('SELECT COUNT(*) FROM queries')
    total_queries = cursor.fetchone()[0]
    
    # Successful queries
    cursor.execute('SELECT COUNT(*) FROM queries WHERE status = "success"')
    successful_queries = cursor.fetchone()[0]
    
    # Failed queries
    cursor.execute('SELECT COUNT(*) FROM queries WHERE status = "failed"')
    failed_queries = cursor.fetchone()[0]
    
    # Most common case types
    cursor.execute('''
        SELECT case_type, COUNT(*) as count
        FROM queries
        GROUP BY case_type
        ORDER BY count DESC
        LIMIT 5
    ''')
    top_case_types = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_queries': total_queries,
        'successful_queries': successful_queries,
        'failed_queries': failed_queries,
        'success_rate': (successful_queries / total_queries * 100) if total_queries > 0 else 0,
        'top_case_types': top_case_types
    }