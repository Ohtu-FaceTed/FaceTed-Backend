#!/bin/bash
python -c 'import os;print(f"SECRET_KEY = {os.urandom(16)}")' > secret_key.py