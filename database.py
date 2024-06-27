import pyodbc

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

    def get_all_comic_code(self):
        try:
            query = "SELECT code FROM Manga;"
            self.cursor.execute(query)
            comic_codes = [row[0] for row in self.cursor.fetchall()]
            return comic_codes
        except Exception as e:
            print("Error occurred while fetching comic codes:", e)
            return []

    def get_track_comic_code(self):
        try:
            query = "SELECT code FROM Manga WHERE track=TRUE;"
            self.cursor.execute(query)
            comic_codes = [row[0] for row in self.cursor.fetchall()]
            return comic_codes
        except Exception as e:
            print("Error occurred while fetching comic codes:", e)
            return []
        
    def insert_data(self, info):
        try:
            # Insert data into Manga table
            insert_query = "INSERT INTO Manga (code, name, score, latest_ch_code, latest_ch_name) VALUES (?, ?, ?, ?, ?);"
            self.cursor.execute(insert_query, (info['code'], info['name'], info['score'], info['latest_ch_code'], info['latest_ch_name']))
            self.conn.commit()
            return "=====Data inserted successfully=====\n漫畫名: {}\n評分: {}\n最近更新: {}".format(info['name'], info['score'], info['latest_ch_name'])
        except Exception as e:
            return f"Error occurred while inserting data: {e}"

    def delete_comic_instances(self, comic_id):
        try:
            # Delete entry in Manga table
            delete_query = "DELETE FROM Manga WHERE id = ?;"
            self.cursor.execute(delete_query, (comic_id,))
            self.conn.commit()
            print(f"Deleted comic ID {comic_id} from Manga table.")
        except Exception as e:
            print("Error occurred while deleting comic instances:", e)
    
    def check_comic_update(self, comic_code, new_chapter_code, new_chapter_name):
        msg = ''
        try:
            # Check the last chapter code stored in database
            query = "SELECT id, name, latest_ch_code, latest_ch_name FROM Manga WHERE code = ?;"
            self.cursor.execute(query, (comic_code,))
            row = self.cursor.fetchone()
            print(row)
            if row:
                comic_id, comic_name, latest_chapter_code, latest_chapter_name = row
                if latest_chapter_code != new_chapter_code:
                    self.update_comic_chapter(comic_id, comic_name, latest_chapter_code, latest_chapter_name, new_chapter_code, new_chapter_name)
                    msg = f"[{comic_name}]: {new_chapter_name}\nhttps://m.happymh.com/reads/{comic_code}/{new_chapter_code}"
                else:
                    print(f"No updates for {comic_name}")
            return msg
        except Exception as e:
            print("Error occurred while checking comic updates:", e)
            return msg

    def update_comic_chapter(self, comic_id, comic_name, old_chapter_code, old_chapter_name, new_chapter_code, new_chapter_name):
        try:
            # Update chapter information in the Manga table
            update_query = "UPDATE Manga SET latest_ch_code = ?, latest_ch_name = ? WHERE id = ?;"
            self.cursor.execute(update_query, (new_chapter_code, new_chapter_name, comic_id))
            self.conn.commit()
            print(f"Updated {comic_name}: {old_chapter_code} -> {new_chapter_code} and {old_chapter_name} -> {new_chapter_name}.")
        except Exception as e:
            print("Error occurred while updating comic chapter:", e)


if __name__ == "__main__":
    pass