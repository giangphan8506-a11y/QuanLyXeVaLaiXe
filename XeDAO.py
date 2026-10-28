from Database import Database


class XeDAO:
    def __init__(self):
        db = Database()
        self.conn = db.get_connection()

    def get_all(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT *
                FROM Xe
                ORDER BY MaXe
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    def tim_xe_theo_ma(self, maxe):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Xe WHERE MaXe = ?", maxe)
            return cursor.fetchone()
        finally:
            cursor.close()

    def tim_xe_theo_ten(self, tenxe):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Xe WHERE TenXe LIKE ? ORDER BY MaXe", '%' + tenxe + '%')
            return cursor.fetchall()
        finally:
            cursor.close()

    def them_xe(self, maxe, bienso, tenxe, maloai, trangthai):
        if not all([maxe and maxe.strip(), bienso and bienso.strip(), tenxe and tenxe.strip(), maloai and maloai.strip()]):
            return False
        if trangthai not in ["Đang hoạt động", "Bảo trì", "Ngừng hoạt động"]:
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Xe (MaXe, BienSo, TenXe, MaLoai, TrangThai)
                VALUES (?, ?, ?, ?, ?)
            """, maxe.strip(), bienso.strip(), tenxe.strip(), maloai.strip(), trangthai)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI THÊM XE:", e)
            return False
        finally:
            cursor.close()

    def sua_xe(self, maxe, bienso, tenxe, maloai, trangthai):
        if not all([maxe and maxe.strip(), bienso and bienso.strip(), tenxe and tenxe.strip(), maloai and maloai.strip()]):
            return False
        if trangthai not in ["Đang hoạt động", "Bảo trì", "Ngừng hoạt động"]:
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT TrangThai FROM Xe WHERE MaXe = ?", maxe)
            xe = cursor.fetchone()
            if xe is None:
                return False

            # Khi có phân công hoạt động, không được đổi trạng thái xe.
            if xe[0] != trangthai:
                cursor.execute("""
                    SELECT 1 FROM PhanCong
                    WHERE MaXe = ? AND TrangThai = N'Đang phân công'
                """, maxe)
                if cursor.fetchone() is not None:
                    return False

            cursor.execute("""
                UPDATE Xe
                SET BienSo = ?, TenXe = ?, MaLoai = ?, TrangThai = ?
                WHERE MaXe = ?
            """, bienso.strip(), tenxe.strip(), maloai.strip(), trangthai, maxe)
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI SỬA XE:", e)
            return False
        finally:
            cursor.close()

    def xoa_xe(self, maxe):
        cursor = self.conn.cursor()
        try:
            # Giữ nguyên lịch sử: không xóa xe đã từng xuất hiện trong phân công.
            cursor.execute("SELECT 1 FROM PhanCong WHERE MaXe = ?", maxe)
            if cursor.fetchone() is not None:
                return False
            cursor.execute("DELETE FROM Xe WHERE MaXe = ?", maxe)
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("LỖI XÓA XE:", e)
            return False
        finally:
            cursor.close()

    def thong_ke_xe(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT TrangThai, COUNT(*) FROM Xe GROUP BY TrangThai")
            return cursor.fetchall()
        finally:
            cursor.close()
