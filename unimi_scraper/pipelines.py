import sqlite3
import hashlib

class SQLitePipeline:
    def open_spider(self, spider):
        # apertura del DB SQLite (o crearne uno nuovo)
        self.conn = sqlite3.connect("unimi_pages.db")
        self.cursor = self.conn.cursor()
        # crea tabella se non esiste
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                shaurl TEXT PRIMARY KEY,
                url TEXT UNIQUE,
                title TEXT,
                html TEXT
            );
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def url_to_sha(self, url: str) -> str:
        # calcola sha256 (o sha1) dall’URL e restituisci stringa esadecimale
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def process_item(self, item, spider):
        try:
            sha = self.url_to_sha(item['url'])
            self.cursor.execute("""
                INSERT OR IGNORE INTO pages (shaurl, url, title, html)
                VALUES (?, ?, ?, ?)
            """, (sha, item['url'], item.get('title'), item.get('html')))
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error saving item: {e}")
        return item