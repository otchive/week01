from flask import Flask, redirect, url_for, session

from config import Config
from routes.auth import auth_bp
from routes.closet import closet_bp
from routes.mypage import mypage_bp

app = Flask(__name__)
app.config.from_object(Config)

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(closet_bp, url_prefix="/closet")
app.register_blueprint(mypage_bp, url_prefix="/mypage")

@app.route("/")
def index():
    # session.pop('user_id', None)
    #로그인 유무에 따라 화면 이동
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("closet.index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

