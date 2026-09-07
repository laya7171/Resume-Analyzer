from app.database.db_connection import get_connection
from rich import print


def fetch_job_tool():
    """
    Fetches all job records from the database and returns them as a list of dictionary"""

    conn = get_connection()
    query = "SELECT * FROM jobs"
    cursor = conn.cursor()
    result = cursor.execute(query).fetchall()

    conn.close()

    return result

