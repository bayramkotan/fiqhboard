"""The application icon, drawn rather than shipped: a lapis tile with فقه in gold Amiri."""

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPainterPath, QPen, QPixmap

LAPIS, GOLD, DEEP = "#1D4777", "#D6B25E", "#14304F"


def pixmap(size: int = 256) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    r = size * 0.22
    tile = QPainterPath()
    tile.addRoundedRect(QRectF(0, 0, size, size), r, r)
    p.fillPath(tile, QColor(DEEP))
    inner = QPainterPath()
    m = size * 0.06
    inner.addRoundedRect(QRectF(m, m, size - 2 * m, size - 2 * m), r * 0.8, r * 0.8)
    p.fillPath(inner, QColor(LAPIS))
    p.setPen(QPen(QColor(GOLD), max(1.0, size * 0.012)))
    p.drawPath(inner)
    font = QFont("Amiri")
    font.setPixelSize(int(size * 0.46))
    font.setBold(True)
    p.setFont(font)
    p.setPen(QColor(GOLD))
    p.drawText(QRectF(0, -size * 0.04, size, size), Qt.AlignmentFlag.AlignCenter, "فقه")
    p.end()
    return pm


def app_icon() -> QIcon:
    icon = QIcon()
    for s in (16, 24, 32, 48, 64, 128, 256):
        icon.addPixmap(pixmap(s))
    return icon
