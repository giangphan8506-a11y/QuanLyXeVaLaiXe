CREATE DATABASE QuanLyXeLaiXe;
GO

USE QuanLyXeLaiXe;
GO

-- ==================================================
-- 2. TAO BANG LOAI XE
-- ==================================================

CREATE TABLE LoaiXe
(
    MaLoai VARCHAR(10) PRIMARY KEY,
    TenLoai NVARCHAR(50) NOT NULL
);
GO

-- ==================================================
-- 3. TAO BANG LAI XE
-- ==================================================

CREATE TABLE LaiXe
(
    MaLaiXe VARCHAR(10) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15),
    SoGPLX VARCHAR(20) NOT NULL UNIQUE,
    LoaiBang VARCHAR(10) NOT NULL,
    TrangThai NVARCHAR(30) NOT NULL
);
GO

-- ==================================================
-- 4. TAO BANG XE
-- ==================================================

CREATE TABLE Xe
(
    MaXe VARCHAR(10) PRIMARY KEY,
    BienSo VARCHAR(15) NOT NULL UNIQUE,
    TenXe NVARCHAR(100) NOT NULL,
    MaLoai VARCHAR(10) NOT NULL,
    TrangThai NVARCHAR(30) NOT NULL,

    CONSTRAINT FK_Xe_LoaiXe
        FOREIGN KEY (MaLoai)
        REFERENCES LoaiXe(MaLoai)
);
GO

-- ==================================================
-- 5. TAO BANG PHAN CONG
-- ==================================================

CREATE TABLE PhanCong
(
    MaPhanCong INT IDENTITY(1,1) PRIMARY KEY,
    MaLaiXe VARCHAR(10) NOT NULL,
    MaXe VARCHAR(10) NOT NULL,
    NgayPhanCong DATE NOT NULL,
    NgayKetThuc DATE NULL,
    TrangThai NVARCHAR(30) NOT NULL,

    CONSTRAINT FK_PhanCong_LaiXe
        FOREIGN KEY (MaLaiXe)
        REFERENCES LaiXe(MaLaiXe),

    CONSTRAINT FK_PhanCong_Xe
        FOREIGN KEY (MaXe)
        REFERENCES Xe(MaXe),

    CONSTRAINT CK_PhanCong_Ngay
        CHECK
        (
            NgayKetThuc IS NULL
            OR NgayKetThuc >= NgayPhanCong
        ),

    CONSTRAINT CK_PhanCong_TrangThai
        CHECK
        (
            (TrangThai = N'Đang phân công'
                AND NgayKetThuc IS NULL)
            OR
            (TrangThai = N'Đã kết thúc'
                AND NgayKetThuc IS NOT NULL)
        )
);
GO

-- ==================================================
-- 6. THEM 3 LOAI XE
-- ==================================================

INSERT INTO LoaiXe (MaLoai, TenLoai)
VALUES
('L01', N'Xe 4 chỗ'),
('L02', N'Xe 5 chỗ'),
('L03', N'Xe 7 chỗ');
GO

-- ==================================================
-- 7. THEM 5 XE
-- ==================================================

INSERT INTO Xe
    (MaXe, BienSo, TenXe, MaLoai, TrangThai)
VALUES
('X01', '67A-10001', N'Toyota Vios',
 'L01', N'Đang hoạt động'),

('X02', '67A-10002', N'Toyota Camry',
 'L02', N'Đang hoạt động'),

('X03', '67A-10003', N'Toyota Innova',
 'L03', N'Đang hoạt động'),

('X04', '67A-10004', N'Toyota Fortuner',
 'L03', N'Bảo trì'),

('X05', '67A-10005', N'Toyota Hilux',
 'L02', N'Ngừng hoạt động');
GO

-- ==================================================
-- 8. THEM 5 LAI XE
-- ==================================================

INSERT INTO LaiXe
    (MaLaiXe, HoTen, SoDienThoai,
     SoGPLX, LoaiBang, TrangThai)
VALUES
('LX01', N'Nguyễn Văn An',
 '0901000001', '790100000001',
 'B2', N'Đang làm việc'),

('LX02', N'Trần Văn Bình',
 '0901000002', '790100000002',
 'B2', N'Đang làm việc'),

('LX03', N'Lê Minh Cường',
 '0901000003', '790100000003',
 'C', N'Đang làm việc'),

('LX04', N'Phạm Văn Dũng',
 '0901000004', '790100000004',
 'B2', N'Tạm nghỉ'),

('LX05', N'Võ Hoàng Nam',
 '0901000005', '790100000005',
 'C', N'Đang làm việc');
GO

-- ==================================================
-- 9. THEM 3 PHAN CONG
-- ==================================================

INSERT INTO PhanCong
    (MaLaiXe, MaXe, NgayPhanCong,
     NgayKetThuc, TrangThai)
VALUES
-- Phan cong dang hoat dong
('LX01', 'X01', '2026-10-01',
 NULL, N'Đang phân công'),

('LX02', 'X02', '2026-10-05',
 NULL, N'Đang phân công'),

-- Phan cong da ket thuc
('LX03', 'X03', '2026-09-01',
 '2026-09-10', N'Đã kết thúc');
GO

-- ==================================================
-- 10. NGAN TRUNG PHAN CONG DANG HOAT DONG
-- ==================================================

CREATE UNIQUE INDEX UX_PhanCong_Xe_DangPhanCong
ON PhanCong (MaXe)
WHERE TrangThai = N'Đang phân công';
GO

CREATE UNIQUE INDEX UX_PhanCong_LaiXe_DangPhanCong
ON PhanCong (MaLaiXe)
WHERE TrangThai = N'Đang phân công';
GO

-- ==================================================
-- 11. KIEM TRA DU LIEU
-- ==================================================

SELECT * FROM LoaiXe;
SELECT * FROM Xe;
SELECT * FROM LaiXe;
SELECT * FROM PhanCong;
GO

SELECT N'Loại xe' AS TenBang, COUNT(*) AS SoLuong
FROM LoaiXe
UNION ALL
SELECT N'Xe', COUNT(*) FROM Xe
UNION ALL
SELECT N'Lái xe', COUNT(*) FROM LaiXe
UNION ALL
SELECT N'Phân công', COUNT(*) FROM PhanCong;
GO