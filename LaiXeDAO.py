from Database import Database


class LaiXeDAO:
    def __init__(self):
        db = Database()
        self.conn = db.get_connection()

    def get_all(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM LaiXe ORDER BY MaLaiXe")
            return cursor.fetchall()
        finally:
            cursor.close()

    def them_lai_xe(self, malaixe, hoten, sodienthoai, sogplx, loaibang, trangthai):
        if not all([malaixe and malaixe.strip(), hoten and hoten.strip(), sogplx and sogplx.strip(), loaibang and loaibang.strip()]):
            return False
        if trangthai not in ["Đang làm việc", "Tạm nghỉ"]:
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO LaiXe (MaLaiXe, HoTen, SoDienThoai, SoGPLX, LoaiBang, TrangThai)
                VALUES (?, ?, ?, ?, ?, ?)
            """, malaixe.strip(), hoten.strip(), sodienthoai, sogplx.strip(), loaibang.strip(), trangthai)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI THÊM LÁI XE:", e)
            return False
        finally:
            cursor.close()

    def tim_lai_xe_theo_ma(self, malaixe):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """SELECT * 
                FROM LaiXe 
                WHERE MaLaiXe = ?
                """
                , malaixe)
            return cursor.fetchone()
        finally:
            cursor.close()

    def tim_lai_xe_theo_ten (self, hoten):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                SELECT *            
                FROM LaiXe 
                WHERE HoTen LIKE ?
                """, '%' + hoten + '%'
            )
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()

    def sua_lai_xe(self, malaixe, hoten, sodienthoai, sogplx, loaibang, trangthai):
        if not all([malaixe and malaixe.strip(), hoten and hoten.strip(), sogplx and sogplx.strip(), loaibang and loaibang.strip()]):
            return False
        if trangthai not in ["Đang làm việc", "Tạm nghỉ"]:
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute("""SELECT TrangThai 
            FROM LaiXe 
            WHERE MaLaiXe = ?
            """, malaixe)
            laixe = cursor.fetchone()
            if laixe is None:
                return False
            # Không cho đổi trạng thái lái xe khi đang có phân công hoạt động.
            if laixe[0] != trangthai:
                cursor.execute("""
                    SELECT 1 FROM PhanCong
                    WHERE MaLaiXe = ? AND TrangThai = N'Đang phân công'
                """, malaixe)
                if cursor.fetchone() is not None:
                    return False
            cursor.execute("""
                UPDATE LaiXe
                SET HoTen = ?, SoDienThoai = ?, SoGPLX = ?, LoaiBang = ?, TrangThai = ?
                WHERE MaLaiXe = ?
            """, hoten.strip(), sodienthoai, sogplx.strip(), loaibang.strip(), trangthai, malaixe)
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI SỬA LÁI XE:", e)
            return False
        finally:
            cursor.close()

    def xoa_lai_xe(self, malaixe):
        cursor = self.conn.cursor()
        try:
            # Không xóa hồ sơ đã có lịch sử phân công.
            cursor.execute("""SELECT 1 
            FROM PhanCong 
            WHERE MaLaiXe = ?
            """, malaixe)
            if cursor.fetchone() is not None:
                return False
            cursor.execute("DELETE FROM LaiXe WHERE MaLaiXe = ?", malaixe)
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI XÓA LÁI XE:", e)
            return False
        finally:
            cursor.close()

    def thong_ke_lai_xe(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
            """SELECT TrangThai, COUNT(*) 
            FROM LaiXe 
            GROUP BY TrangThai
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
