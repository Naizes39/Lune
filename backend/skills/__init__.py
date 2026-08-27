# skills/__init__.py

"""
Registry of all skills for Lune.
"""


from backend.skills.local_tools import read_file, write_file
from backend.skills.web_search import web_search

SKILLS_REGISTRY = {
    "read_file": read_file,
    "write_file": write_file,
    "web_search": web_search
}

