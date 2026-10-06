#!/usr/bin/env python
"""
URBAN THREADS — Website Bán Thời Trang Streetwear
==================================================
PHIA SAU  (Backend)  : Django 5.1.1 | Python 3.10+ | Kiến trúc MVT
PHIA TRUOC (Frontend): Tailwind CSS v3 (CDN) + Alpine.js v3 (CDN) + HTML5
CO SO DU LIEU (DB)   : SQLite | File: db.sqlite3
CONG THANH TOAN      : VietQR API (Napas247) — đa ngân hàng Việt Nam
ENTRY POINT          : python manage.py runserver
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_threads.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
