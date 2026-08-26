from flask import Blueprint, render_template, request, jsonify, session
from db import items

mypage_bp = Blueprint("mypage", __name__)

@mypage_bp.route("/")
def mypage():
    user_id = session.get("user_id")

    stats = get_closet_stats(user_id)

    return render_template('mypage/index.html', user=user_id, stats=stats)


def get_closet_stats(user_id):

    pipeline = [
        {"$match": {"user_id": user_id}},
        
        {
            "$group": {
                "_id": "$user_id",
                "total_count": {"$sum": 1},
                "total_price": {"$sum": "$price"}
            }
        }
    ]

    result = list(items.aggregate(pipeline))

    if result:
        total_count = result[0]["total_count"]
        total_price = result[0]["total_price"]
    else:
        total_count = 0
        total_price = 0

    most_worn_item = items.find_one(
        {"user_id": user_id},
        sort=[("wear_count", -1)]
    )
    least_worn_item = items.find_one(
        {"user_id": user_id},
        sort=[("wear_count", 1)]
    )

    return {
        "total_count": total_count,
        "total_price": total_price,
        "most_worn": most_worn_item.get("name") if most_worn_item else "없음",
        "least_worn": least_worn_item.get("name") if least_worn_item else "없음"
    }

