
from Database import Database


class PhanCongDAO(Database):

    def __init__(self):
        db = Database()
        self.conn = db.get_connection()

    # ==========================================
    # LẤY TẤT CẢ PHÂN CÔNG
    # ==========================================
    def get_all(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT *
                FROM PhanCong
                ORDER BY MaPhanCong DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()

    # ==========================================
    # TÌM PHÂN CÔNG THEO MÃ
    # ==========================================
    def tim_phancong_theo_ma(self, maphancong):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
                SELECT *
                FROM PhanCong
                WHERE MaPhanCong = ?
                """,
                (maphancong,)
            )

            return cursor.fetchone()

        finally:
            cursor.close()

    # ==========================================
    # THÊM PHÂN CÔNG
    # ==========================================
    def them_phancong(
        self,
        malaixe,
        maxe,
        ngayphancong,
        ngayketthuc,
        trangthai
    ):
        cursor = self.conn.cursor()

        try:
            # 1. Kiểm tra xe
            cursor.execute(
                """
                SELECT TrangThai
                FROM Xe
                WHERE MaXe = ?
                """,
                (maxe,)
            )

            xe = cursor.fetchone()

            if xe is None:
                return False

            # 2. Xe phải đang hoạt động
            if trangthai == "Đang phân công":
                if xe[0] != "Đang hoạt động":
                    return False

            # 3. Kiểm tra lái xe
            cursor.execute(
                """
                SELECT TrangThai
                FROM LaiXe
                WHERE MaLaiXe = ?
                """,
                (malaixe,)
            )

            laixe = cursor.fetchone()

            if laixe is None:
                return False

            # 4. Lái xe phải đang làm việc
            if trangthai == "Đang phân công":
                if laixe[0] != "Đang làm việc":
                    return False

            # 5. Kiểm tra trạng thái và ngày kết thúc
            if trangthai == "Đang phân công":
                ngayketthuc = None

            elif trangthai == "Đã kết thúc":

                if ngayketthuc is None or ngayketthuc == "":
                    return False

                cursor.execute(
                    """
                    SELECT 1
                    WHERE CAST(? AS DATE) < CAST(? AS DATE)
                    """,
                    (ngayketthuc, ngayphancong)
                )

                if cursor.fetchone() is not None:
                    return False

            else:
                return False

            # 6. Kiểm tra xe đã được phân công chưa
            if trangthai == "Đang phân công":
                cursor.execute(
                    """
                    SELECT MaPhanCong
                    FROM PhanCong
                    WHERE MaXe = ?
                      AND TrangThai = N'Đang phân công'
                    """,
                    (maxe,)
                )

                if cursor.fetchone() is not None:
                    return False

            # 7. Kiểm tra lái xe đã được phân công chưa
            if trangthai == "Đang phân công":
                cursor.execute(
                    """
                    SELECT MaPhanCong
                    FROM PhanCong
                    WHERE MaLaiXe = ?
                      AND TrangThai = N'Đang phân công'
                    """,
                    (malaixe,)
                )

                if cursor.fetchone() is not None:
                    return False

            # 8. Thêm phân công
            cursor.execute(
                """
                INSERT INTO PhanCong
                (
                    MaLaiXe,
                    MaXe,
                    NgayPhanCong,
                    NgayKetThuc,
                    TrangThai
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    malaixe,
                    maxe,
                    ngayphancong,
                    ngayketthuc,
                    trangthai
                )
            )

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print("LỖI THÊM PHÂN CÔNG:", e)
            return False

        finally:
            cursor.close()

    # ==========================================
    # SỬA PHÂN CÔNG
    # ==========================================
    def sua_phancong(
        self,
        maphancong,
        malaixe,
        maxe,
        ngayphancong,
        ngayketthuc,
        trangthai
    ):
        cursor = self.conn.cursor()

        try:
            # 1. Kiểm tra phân công có tồn tại không
            cursor.execute(
                """
                SELECT TrangThai
                FROM PhanCong
                WHERE MaPhanCong = ?
                """,
                (maphancong,)
            )

            pc = cursor.fetchone()

            if pc is None:
                return False

            # Không sửa phân công đã kết thúc
            if pc[0] == "Đã kết thúc":
                return False

            # 2. Kiểm tra xe
            cursor.execute(
                """
                SELECT TrangThai
                FROM Xe
                WHERE MaXe = ?
                """,
                (maxe,)
            )

            xe = cursor.fetchone()

            if xe is None:
                return False

            if trangthai == "Đang phân công":
                if xe[0] != "Đang hoạt động":
                    return False

            # 3. Kiểm tra lái xe
            cursor.execute(
                """
                SELECT TrangThai
                FROM LaiXe
                WHERE MaLaiXe = ?
                """,
                (malaixe,)
            )

            laixe = cursor.fetchone()

            if laixe is None:
                return False

            if trangthai == "Đang phân công":
                if laixe[0] != "Đang làm việc":
                    return False

            # 4. Kiểm tra ngày kết thúc
            if trangthai == "Đang phân công":
                ngayketthuc = None

            elif trangthai == "Đã kết thúc":

                if ngayketthuc is None or ngayketthuc == "":
                    return False

                cursor.execute(
                    """
                    SELECT 1
                    WHERE CAST(? AS DATE) < CAST(? AS DATE)
                    """,
                    (ngayketthuc, ngayphancong)
                )

                if cursor.fetchone() is not None:
                    return False

            else:
                return False

            # 5. Kiểm tra xe đang được phân công
            if trangthai == "Đang phân công":
                cursor.execute(
                    """
                    SELECT MaPhanCong
                    FROM PhanCong
                    WHERE MaXe = ?
                      AND TrangThai = N'Đang phân công'
                      AND MaPhanCong <> ?
                    """,
                    (maxe, maphancong)
                )

                if cursor.fetchone() is not None:
                    return False

            # 6. Kiểm tra lái xe đang được phân công
            if trangthai == "Đang phân công":
                cursor.execute(
                    """
                    SELECT MaPhanCong
                    FROM PhanCong
                    WHERE MaLaiXe = ?
                      AND TrangThai = N'Đang phân công'
                      AND MaPhanCong <> ?
                    """,
                    (malaixe, maphancong)
                )

                if cursor.fetchone() is not None:
                    return False

            # 7. Cập nhật phân công
            cursor.execute(
                """
                UPDATE PhanCong
                SET
                    MaLaiXe = ?,
                    MaXe = ?,
                    NgayPhanCong = ?,
                    NgayKetThuc = ?,
                    TrangThai = ?
                WHERE MaPhanCong = ?
                """,
                (
                    malaixe,
                    maxe,
                    ngayphancong,
                    ngayketthuc,
                    trangthai,
                    maphancong
                )
            )

            if cursor.rowcount == 0:
                self.conn.rollback()
                return False

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print("LỖI SỬA PHÂN CÔNG:", e)
            return False

        finally:
            cursor.close()

    # ==========================================
    # XÓA PHÂN CÔNG
    # ==========================================
    def Xoa_phancong(self, maphancong):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM PhanCong
                WHERE MaPhanCong = ?
                """,
                (maphancong,)
            )

            if cursor.rowcount == 0:
                self.conn.rollback()
                return False

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print("LỖI XÓA PHÂN CÔNG:", e)
            return False

        finally:
            cursor.close()

    # ==========================================
    # XEM PHÂN CÔNG CHI TIẾT
    # ==========================================
    def xem_phan_cong_chi_tiet(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    PC.MaPhanCong,
                    LX.MaLaiXe,
                    LX.HoTen,
                    X.MaXe,
                    X.BienSo,
                    X.TenXe,
                    PC.NgayPhanCong,
                    PC.NgayKetThuc,
                    PC.TrangThai
                FROM PhanCong PC
                INNER JOIN LaiXe LX
                    ON PC.MaLaiXe = LX.MaLaiXe
                INNER JOIN Xe X
                    ON PC.MaXe = X.MaXe
                ORDER BY PC.MaPhanCong DESC
                """
            )

            return cursor.fetchall()

        finally:
            cursor.close()

    def get_laixe_du_dieu_kien(self, maphancong=None):
        cursor = self.conn.cursor()

        try:
            sql = """
                SELECT LX.MaLaiXe, LX.HoTen
                FROM LaiXe LX
                WHERE LX.TrangThai = N'Đang làm việc'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM PhanCong PC
                      WHERE PC.MaLaiXe = LX.MaLaiXe
                        AND PC.TrangThai = N'Đang phân công'
            """

            params = []

            if maphancong is not None:
                sql += " AND PC.MaPhanCong <> ?"
                params.append(maphancong)

            sql += """
                  )
                ORDER BY LX.MaLaiXe
            """

            cursor.execute(sql, tuple(params))
            return cursor.fetchall()

        finally:
            cursor.close()

    def get_xe_du_dieu_kien(self, maphancong=None):
        cursor = self.conn.cursor()

        try:
            sql = """
                SELECT X.MaXe, X.BienSo, X.TenXe
                FROM Xe X
                WHERE X.TrangThai = N'Đang hoạt động'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM PhanCong PC
                      WHERE PC.MaXe = X.MaXe
                        AND PC.TrangThai = N'Đang phân công'
            """

            params = []

            if maphancong is not None:
                sql += " AND PC.MaPhanCong <> ?"
                params.append(maphancong)

            sql += """
                  )
                ORDER BY X.MaXe
            """

            cursor.execute(sql, tuple(params))
            return cursor.fetchall()

        finally:
            cursor.close()
