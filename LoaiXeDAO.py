from Database import Database


class LoaiXeDAO:
    def __init__(self):
        db = Database()
        self.conn = db.get_connection()

    def get_all(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM LoaiXe ORDER BY MaLoai")
            return cursor.fetchall()
        finally:
            cursor.close()

    def tim_loai_xe_theo_ma(self, maloai):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM LoaiXe WHERE MaLoai = ?", maloai)
            return cursor.fetchone()
        finally:
            cursor.close()

    def them_loai_xe(self, maloai, tenloai):
        if not (maloai and maloai.strip() and tenloai and tenloai.strip()):
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO LoaiXe (MaLoai, TenLoai) VALUES (?, ?)", maloai.strip(), tenloai.strip())
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI THÊM LOẠI XE:", e)
            return False
        finally:
            cursor.close()

    def sua_loai_xe(self, maloai, tenloai):
        if not (tenloai and tenloai.strip()):
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE LoaiXe SET TenLoai = ? WHERE MaLoai = ?", tenloai.strip(), maloai)
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI SỬA LOẠI XE:", e)
            return False
        finally:
            cursor.close()

    def xoa_loai_xe(self, maloai):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM Xe WHERE MaLoai = ?", maloai)
            if cursor.fetchone() is not None:
                return False
            cursor.execute("DELETE FROM LoaiXe WHERE MaLoai = ?", maloai)
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI XÓA LOẠI XE:", e)
            return False
        finally:
            cursor.close()
