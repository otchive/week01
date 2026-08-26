from flask import Blueprint, render_template, request, jsonify, session
from services.closet_service import create_closet_item
from bson.objectid import ObjectId
from db import items

from db import *

closet_bp = Blueprint("closet", __name__)

cloth_type_id = {'상의': 1, '하의': 2, '외투': 3, '신발': 4, '악세서리': 5}

@closet_bp.route('/', methods=['GET'])
def index():
    button_ctrl = [False for _ in range(6)]
    cloth_type = request.args.get('type')
    user = session['user_id']
    if cloth_type:
        closet_items = items.find({'user_id': user, 'type': cloth_type})
        button_ctrl[cloth_type_id.get(cloth_type)] = True
    else:
        closet_items = items.find({'user_id': user})
        button_ctrl[0] = True
    return render_template('closet/index.html', user=user, items=closet_items, btn_ctrl=button_ctrl)


# 등록 API
@closet_bp.route("/register", methods=["GET", "POST"])
def register_item():

    if request.method == "POST":
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"message": "로그인 하세요."}), 401

        if "file" not in request.files or request.files["file"].filename == "":
            return jsonify({"message": "이미지 파일이 필요합니다."}), 400

        try:
            file = request.files["file"]
            item_id = create_closet_item(user_id, request.form, file)
            return jsonify({"message": "성공적으로 등록되었습니다.", "item_id": item_id}), 201
        
        except Exception as e:
            return jsonify({"message": f"등록 실패: {str(e)}"}), 500
        
    return render_template("closet/register.html")


# 옷 상세 페이지
@closet_bp.route("/<item_id>/detail", methods=["GET"])
def get_item(item_id):
    user = session['user_id']

    try:
        item = items.find_one({
            "_id": ObjectId(item_id)
        })
    except Exception:
        return "잘못된 옷 ID입니다.", 400

    if not item:
        return "옷을 찾을 수 없습니다.", 404

    item["_id"] = str(item["_id"])

    return render_template(
        "closet/detail.html",
        user=user,
        item=item
    )


# 옷 상세 - 수정 API
@closet_bp.route("/<item_id>/edit", methods=["POST"])
def fix_item(item_id):
    #try-except로 리팩토링
    
    items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {
                "name": request.form.get("name"),
                "brand": request.form.get("brand"),
                "type": request.form.get("type"),
                "size": request.form.get("size"),
                "season": request.form.get("season"),
                "buy_date": request.form.get("buy_date"),
                "price": request.form.get("price"),
                "buy_method": request.form.get("buy_method")
            }}
        )

    return jsonify({"message": "수정 완료"}), 200

# 옷 상세 - 삭제 API
@closet_bp.route("/<item_id>/delete", methods=["DELETE"])
def delete_item(item_id):
    items.delete_one({"_id": ObjectId(item_id)})
    return jsonify({"message": "삭제 완료"}), 200

#옷 상세 - 오늘 입었어요 API
@closet_bp.route("/<item_id>/wear", methods=["POST"])
def wear_item(item_id):
    try:
        result = items.update_one({"_id": ObjectId(item_id)},
                     {"$inc": {"wear_count": 1}
                      })

    except Exception:
        return jsonify({"message": "잘못된 옷 ID입니다."}), 400

    if result.matched_count == 0:
        return jsonify({"message": "옷을 찾을 수 없습니다."}), 404

    item = items.find_one(
        {"_id": ObjectId(item_id)},
        {"wear_count": 1}
    )

    return jsonify({
        "message": "착용 횟수가 증가했습니다.",
        "wear_count": item.get("wear_count", 0)
    }), 200
    

#옷 상세 - 인생핏 API
@closet_bp.route("/<item_id>/life-fit", methods=["POST"])
def toggle_life_fit(item_id):
    try:
        result = items.update_one({"_id": ObjectId(item_id)},
                        [
                            {
                                "$set": {
                                    "is_life_fit": {
                                        "$not": "$is_life_fit"
                                    }
                                }
                            }
                        ]
                    )
    
    except Exception:
        return jsonify({"message": "잘못된 옷 ID입니다."}), 400

    if result.matched_count == 0:
        return jsonify({"message": "옷을 찾을 수 없습니다."}), 404

    return jsonify({"message": "업데이트 완료"}), 200

#마이페이지 안 입는 옷 API
@closet_bp.route("/unworn")
def unworn():
    user = session['user_id']
    unworn_list = items.find({'wear_count': 0, 'user_id': user})
    unworn_list = list(unworn_list)
    print(unworn_list)
    return render_template('closet/unworn.html', user=user, unworn_list=unworn_list)

#인생핏 화면
@closet_bp.route('/life-fit')
def life_fit():
    user = session['user_id']
    life_list = items.find({'is_life_fit': True, 'user_id': user})
    life_list = list(life_list)
    print(life_list)
    return render_template('closet/life_fit.html', user=user, life_list=life_list)