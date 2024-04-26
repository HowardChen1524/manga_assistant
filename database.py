import pyodbc

class MyDatabase:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_connection(self):
        conn_str = (
            r'DRIVER={MySQL ODBC 8.0 Unicode Driver};'
            r'SERVER=localhost;'
            r'DATABASE=mybookcase;'
            r'USER=debian-sys-maint;'
            r'PASSWORD=oQ3OX6cw77RuFeIF;'
        )
        try:
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("Successfully connected to database!")
        except Exception as e:
            print("Error occurred while connecting to database:", e)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection closed.")

    def insert_data(self, comic_code, comic_name, comic_score, chapter_code, chapter_name):
        try:
            # Insert data into Comics table
            insert_comics_query = "INSERT INTO Comics (comic_code, comic_name, comic_score) VALUES (?, ?, ?);"
            self.cursor.execute(insert_comics_query, (comic_code, comic_name, comic_score))
            self.conn.commit()

            # Get the last inserted comic ID
            comic_id = self.cursor.execute("SELECT LAST_INSERT_ID();").fetchone()[0]

            # Insert data into Updates table
            insert_updates_query = "INSERT INTO Updates (chapter_code, chapter_name, comic_id) VALUES (?, ?, ?);"
            self.cursor.execute(insert_updates_query, (chapter_code, chapter_name, comic_id))
            self.conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("Error occurred while inserting data:", e)

    def check_comic_update(self, comic_code, new_chapter_code):
        try:
            # Check the last chapter code stored in database
            query = "SELECT u.chapter_code FROM Updates u JOIN Comics c ON u.comic_id = c.id WHERE c.comic_code = ? ORDER BY u.id DESC LIMIT 1;"
            self.cursor.execute(query, (comic_code,))
            last_chapter_code = self.cursor.fetchone()
            if last_chapter_code and last_chapter_code[0] != new_chapter_code:
                print("New update available for comic", comic_code)
                return True
            else:
                print("No new updates for comic", comic_code)
                return False
        except Exception as e:
            print("Error occurred while checking comic updates:", e)
            return False

if __name__ == "__main__":
    db = MyDatabase()
    db.open_connection()
    # db.insert_data('yeyingjiadedazuozhan', '夜樱家的大作战', 4.5, '4302333', '223 军团')
    db.check_comic_update('yeyingjiadedazuozhan', '4302334')
    db.close_connection()
