from models import Harcama
from extensions import db

def harcama_ekle(baslik, miktar, kategori, tarih, kullanici_id):
    yeni_harcama = Harcama(
        baslik=baslik,
        miktar=miktar,
        kategori=kategori,
        tarih=tarih,
        kullanici_id=kullanici_id
    )
    db.session.add(yeni_harcama)
    db.session.commit()
    return yeni_harcama

def harcama_getir(harcama_id):
    return Harcama.query.get_or_404(harcama_id)

def harcama_guncelle(harcama, baslik=None, miktar=None, kategori=None, tarih=None):
    if baslik is not None:
        harcama.baslik = baslik
    if miktar is not None:
        harcama.miktar = miktar
    if kategori is not None:
        harcama.kategori = kategori
    if tarih is not None:
        harcama.tarih = tarih
    db.session.commit()
    return harcama

def harcama_sil(harcama):
    db.session.delete(harcama)
    db.session.commit()
