from flask import Flask,request,jsonify
from models import db,bcrypt,Kullanici,Harcama
from functools import wraps
import jwt
import datetime

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///harcamalar.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="gizli_anahtar"

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

def token_gerekli(f):
    @wraps(f)
    def sarici(*args,**kwargs):
        token=request.headers.get("Authorization")
        if not token:
            return jsonify({"hata":"token gerekli"}),401
        try:
            token=token.replace("Bearer ","")
            data=jwt.decode(token,app.config["SECRET_KEY"],algorithms="HS256")
            kullanici_id=data["kullanici_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"hata":"Token süresi bitmiş"}),401
        except jwt.InvalidTokenError:
            return jsonify({"hata":"Geçersiz token"}),401
        return f(kullanici_id,*args,**kwargs)
    return sarici

@app.route("/kayit",methods=["POST"])
def kayit():
    data=request.json
    kullanici_adi=data.get("kullanici_adi")
    sifre=data.get("sifre")

    if not kullanici_adi or not sifre:
        return jsonify({"hata":"eksik bilgi"}),400
    
    if Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first():
        return jsonify({"hata":"Bu kullanici adi zaten alinmiş"}),401
    
    sifre_hash=bcrypt.generate_password_hash(sifre).decode("utf-8")
    yeni_kisi=Kullanici(kullanici_adi=kullanici_adi,sifre_hash=sifre_hash)
    db.session.add(yeni_kisi)
    db.session.commit()

    return jsonify({"mesaj":"Kayit basarili"}),201


@app.route("/giris",methods=["POST"])
def giris():
    data=request.json
    kullanici_adi=data.get("kullanici_adi")
    sifre=data.get("sifre")

    kullanici=Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
    if not kullanici or not kullanici.sifre_kontrol(sifre):
        return jsonify({"hata":"Geçersiz kullanici_adi yada sifre"}),401
    
    token=jwt.encode(
        {
            "kullanici_id":kullanici.id,
            "exp":datetime.datetime.utcnow() +datetime.timedelta(hours=3)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return jsonify({"token":token})


@app.route("/harcamalar",methods=["POST"])
@token_gerekli()
def harcama_ekle(kullanici_id):
    data=request.json
    baslik=data.get("baslik")
    miktar=data.get("miktar")
    kategori=data.get("kategori")
    tarih=data.get("tarih")

    if not baslik or not miktar or not kategori or not tarih:
        return jsonify({"hata":"Eksik bilgi girilemez"}),400
    
    yeni_harcama=Harcama(baslik=baslik,miktar=miktar,kategori=kategori,tarih=tarih,kullanici_id=kullanici_id)
    db.session.add(yeni_harcama)
    db.session.commit()

    return jsonify({"mesaj":"Harcama eklendi","Harcama":yeni_harcama.to_dict()})



@app.route("/harcamalar",methods=["GET"])
def harcamalari_getir():
    harcamalar=Harcama.query.all()
    return jsonify([k.to_dict() for k in harcamalar])

@app.route("/harcamalar/<int:id>",methods=["GET"])
def harcamayi_getir(id):
    harcama=Harcama.query.get(id)
    if not harcama:
        return jsonify({"hata":"harcama bulunamadi"}),404
    return jsonify(harcama.to_dict())


@app.route("/harcamalar/<int:id>",methods=["PUT"])
@token_gerekli
def harcamayi_guncelle(id,kullanici_id):
    harcama=Harcama.query.filter_by(id=id,kullanici_id=kullanici_id).first()
    if not harcama:
        return jsonify({"hata":"Harcama bulunamadi"}),404
    
    data=request.json
    harcama.baslik=data.get("baslik",harcama.baslik)
    harcama.miktar=data.get("miktar",harcama.miktar)
    harcama.kategori=data.get("kategori",harcama.kategori)
    harcama.tarih=data.get("tarih",harcama.tarih)

    db.session.commit()

    return jsonify({"mesaj":"Harcama güncellendi","Harcama:":harcama.to_dict()})

@app.route("/harcamalar/<int:id>",methods=["DELETE"])
@token_gerekli
def harcamayi_sil(id,kullanici_id):
    harcama=Harcama.query.filter_by(id=id,kullanici_id=kullanici_id).first()
    if not harcama:
        return jsonify({"hata":"Harcama bulunamadi"}),404
    
    db.session.delete(harcama)
    db.session.commit()
    
    return jsonify({"mesaj":"Harcama silindi."})

if __name__=="__main__":
    app.run(debug=True,port=5001)

