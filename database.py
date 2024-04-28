import pyodbc
from collections import defaultdict
class MyDatabase:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_connection(self):
        conn_str = (
            r'DRIVER={MySQL ODBC 8.3 Unicode Driver};'
            r'SERVER=localhost;'
            r'DATABASE=bookcase;'
            r'USER=root;'
            r'PASSWORD=root;'
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

    def insert_data(self, info):
        try:
            self.open_connection()
            # Insert data into Comics table
            insert_comics_query = "INSERT INTO Comics (comic_code, comic_name, comic_score) VALUES (?, ?, ?);"
            self.cursor.execute(insert_comics_query, (info['code'], info['name'], info['score']))
            self.conn.commit()

            # Get the last inserted comic ID
            comic_id = self.cursor.execute("SELECT LAST_INSERT_ID();").fetchone()[0]

            # Insert data into Updates table
            insert_updates_query = "INSERT INTO Updates (chapter_code, chapter_name, comic_id) VALUES (?, ?, ?);"
            self.cursor.execute(insert_updates_query, (info['latest_ch_id'], info['latest_ch_name'], comic_id))
            self.conn.commit()
            self.close_connection()
            return "=====Data inserted successfully=====\n漫畫名: {}\n評分: {}\n最近更新: {}".format(info['name'], info['score'], info['latest_ch_name'])
        except Exception as e:
            return f"Error occurred while inserting data: {e}"
        
    def delete_comic_instances(self, comic_id):
        try:
            # Delete entries in Updates table
            delete_updates_query = "DELETE FROM Updates WHERE comic_id = ?;"
            self.cursor.execute(delete_updates_query, (comic_id,))
            self.conn.commit()

            # Delete entry in Comics table
            delete_comics_query = "DELETE FROM Comics WHERE id = ?;"
            self.cursor.execute(delete_comics_query, (comic_id,))
            self.conn.commit()
            print(f"Deleted all instances of comic ID {comic_id} from Comics and Updates tables.")
        except Exception as e:
            print("Error occurred while deleting comic instances:", e)
    
    def check_comic_update(self, comic_code, new_chapter_code):
        try:
            # Check the last chapter code stored in database
            query = "SELECT u.chapter_code FROM Updates u JOIN Comics c ON u.comic_id = c.id WHERE c.comic_code = ? ORDER BY u.id DESC LIMIT 1;"
            self.cursor.execute(query, (comic_code,))
            last_chapter_code = self.cursor.fetchone()
            if last_chapter_code and last_chapter_code[0] != new_chapter_code:
                print("New update available for comic", comic_code)
                self.update_comic_chapter()
                return True
            else:
                print("No new updates for comic", comic_code)
                return False
        except Exception as e:
            print("Error occurred while checking comic updates:", e)
            return False

    def update_comic_chapter(self, comic_id, new_chapter_code, new_chapter_name):
        try:
            # Update chapter information in the Updates table
            update_query = "UPDATE Updates SET chapter_code = ?, chapter_name = ? WHERE comic_id = ?;"
            self.cursor.execute(update_query, (new_chapter_code, new_chapter_name, comic_id))
            self.conn.commit()
            print(f"Updated comic ID {comic_id} with new chapter code {new_chapter_code} and name {new_chapter_name}.")
        except Exception as e:
            print("Error occurred while updating comic chapter:", e)


if __name__ == "__main__":
    import pyodbc
    # 列出所有可用的 ODBC 驅動
    available_drivers = pyodbc.drivers()
    print("Available ODBC drivers:")
    for driver in available_drivers:
        print(driver)

    pass