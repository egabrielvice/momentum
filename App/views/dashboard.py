import streamlit as st

from database import *
from utils.helpers import *

def dashboard_page():
    programs = get_programs()
    active_program_id = get_active_program_id()

    ...