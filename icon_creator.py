"""
회의록분석기 아이콘 생성기
실행: python icon_creator.py
필요 패키지: pip install Pillow
"""
from PIL import Image, ImageDraw

def create_icon(out_path="icon.ico"):
    SIZE = 256
    img  = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d    = ImageDraw.Draw(img)

    BLUE  = (46, 117, 182, 255)   # #2E75B6 (앱 테마색)
    WHITE = (255, 255, 255, 255)
    FOLD  = (196, 218, 240, 255)  # 접힌 모서리
    GREEN = (16, 124, 65, 255)    # #107C41
    LINE  = (46, 117, 182, 180)

    # ── 파란 배경 (모서리 둥글게) ──
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=44, fill=BLUE)

    # ── 흰 문서 몸체 ──
    FOLD_SZ = 38
    dx1, dy1 = 58, 36
    dx2, dy2 = 198, 220
    d.polygon([
        (dx1, dy1),
        (dx2 - FOLD_SZ, dy1),
        (dx2, dy1 + FOLD_SZ),
        (dx2, dy2),
        (dx1, dy2),
    ], fill=WHITE)

    # ── 접힌 모서리 삼각형 ──
    d.polygon([
        (dx2 - FOLD_SZ, dy1),
        (dx2,           dy1 + FOLD_SZ),
        (dx2 - FOLD_SZ, dy1 + FOLD_SZ),
    ], fill=FOLD)

    # ── 문서 안 텍스트 라인 ──
    lx1 = dx1 + 18
    lx2 = dx2 - 18
    for idx, y in enumerate([90, 112, 134, 156]):
        x2 = lx2 if idx < 3 else lx1 + 72   # 마지막 줄만 짧게
        d.rounded_rectangle([lx1, y, x2, y + 9], radius=4, fill=LINE)

    # ── 초록 체크 뱃지 ──
    cx, cy, cr = 188, 188, 38
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=GREEN)
    # 체크마크
    pts = [(cx - 16, cy + 2), (cx - 4, cy + 14), (cx + 18, cy - 14)]
    d.line(pts, fill=WHITE, width=6)

    # ── 다중 크기 ICO를 바이너리로 직접 빌드 ──
    # (Pillow ICO 플러그인이 sizes 파라미터를 항상 신뢰할 수 없어 직접 구성)
    import struct, io

    SIZES = [16, 32, 48, 256]

    png_blobs = []
    for s in SIZES:
        buf = io.BytesIO()
        img.resize((s, s), Image.LANCZOS).save(buf, format="PNG")
        png_blobs.append(buf.getvalue())

    n = len(SIZES)
    # ICONDIR 헤더 (6 bytes)
    ico = struct.pack("<HHH", 0, 1, n)
    # ICONDIRENTRY 배열 (각 16 bytes): 데이터 위치 = 6 + 16*n + 이전 합계
    offset = 6 + 16 * n
    for s, blob in zip(SIZES, png_blobs):
        w = s if s < 256 else 0   # 256 크기는 ICO 스펙상 0으로 기록
        ico += struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(blob), offset)
        offset += len(blob)
    ico += b"".join(png_blobs)

    with open(out_path, "wb") as f:
        f.write(ico)
    print(f"✅ 아이콘 생성 완료: {out_path}  ({len(ico):,} bytes, {n}가지 크기)")


if __name__ == "__main__":
    create_icon()
