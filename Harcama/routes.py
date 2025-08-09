from flask import Blueprint, request, jsonify
from decorators import token_dogrula
from Harcama.services import harcama_ekle, harcama_getir, harcama_guncelle, harcama_sil
from Harcama.validators import eksik_alan_kontrol
from models import Harcama

harcama_bp = Blueprint("harcamalar", __name__)

@harcama_bp.route("/", methods=["POST"])
@token_dogrula
def harcama_ekle_route():
    veri = request.get_json()
    eksik = eksik_alan_kontrol(veri, ["baslik", "miktar", "kategori", "tarih"])
    if eksik:
        return jsonify({"hata": f"{eksik} alanı eksik"}), 400
    
    yeni_harcama = harcama_ekle(
        veri["baslik"],
        veri["miktar"],
        veri["kategori"],
        veri["tarih"],
        request.kullanici_id
    )
    return jsonify({"mesaj": "Harcama eklendi", "harcama_id": yeni_harcama.id}), 201

@harcama_bp.route("/", methods=["GET"])
@token_dogrula
def harcamalari_getir():
    harcamalar = Harcama.query.filter_by(kullanici_id=request.kullanici_id).all()
    sonuc = [h.to_dict() for h in harcamalar]
    return jsonify(sonuc), 200

@harcama_bp.route("/<int:harcama_id>", methods=["GET"])
@token_dogrula
def harcama_getir_route(harcama_id):
    harcama = Harcama.query.filter_by(id=harcama_id, kullanici_id=request.kullanici_id).first_or_404()
    return jsonify(harcama.to_dict()), 200

@harcama_bp.route("/<int:harcama_id>", methods=["PUT"])
@token_dogrula
def harcama_guncelle_route(harcama_id):
    veri = request.get_json()
    harcama = Harcama.query.filter_by(id=harcama_id, kullanici_id=request.kullanici_id).first_or_404()
    harcama_guncelle(
        harcama,
        veri.get("baslik"),
        veri.get("miktar"),
        veri.get("kategori"),
        veri.get("tarih")
    )
    return jsonify({"mesaj": "Harcama güncellendi"}), 200

@harcama_bp.route("/<int:harcama_id>", methods=["DELETE"])
@token_dogrula
def harcama_sil_route(harcama_id):
    harcama = Harcama.query.filter_by(id=harcama_id, kullanici_id=request.kullanici_id).first_or_404()
    harcama_sil(harcama)
    return jsonify({"mesaj": "Harcama silindi"}), 200
