from extensions import db, bcrypt

class Kullanici(db.Model):
    __tablename__ = "kullanicilar"

    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(100), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(100), nullable=False)

    def sifre_kontrol(self, sifre):
        return bcrypt.check_password_hash(self.sifre_hash, sifre)


class Harcama(db.Model):
    __tablename__ = "harcamalar"

    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    miktar = db.Column(db.Integer, nullable=False)
    kategori = db.Column(db.String(100), nullable=False)
    tarih = db.Column(db.String(100), nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey("kullanicilar.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "baslik": self.baslik,
            "miktar": self.miktar,
            "kategori": self.kategori,
            "tarih": self.tarih,
            "kullanici_id": self.kullanici_id
        }
