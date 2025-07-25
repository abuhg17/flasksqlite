import sqlitecloud
from flask import Flask, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_name = "sqlitegoldshoot0720.db"

@app.get("/")
def index():
    return """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <title>庫存圖片展示</title>
  <style>
    img {
      max-width: 200px;
      margin: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <h1>Inventory 圖片展示</h1>
  <div id="images">載入中...</div>

  <script>
    fetch("/inventory")
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById("images");
        container.innerHTML = ""; // 清空載入中文字
        data.forEach(item => {
          if (item.img1) {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${item.img1}`;
            img.alt = item.name || "圖片";
            container.appendChild(img);
          }
        });
      })
      .catch(error => {
        document.getElementById("images").innerText = "載入失敗：" + error;
        console.error(error);
      });
  </script>
</body>
</html>
"""

def query_table(table_name):
    conn = sqlitecloud.connect(
        "sqlitecloud://cmk0dgzqhk.g2.sqlite.cloud:8860/auth.sqlitecloud?apikey=tFponRnK20mvO37gEImnuRCuVLDFvydAbbopxaVkXPg"
    )
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

@app.route('/subscription')
def get_subscription():
    return jsonify(query_table("subscription"))

@app.route('/mail')
def get_mail():
    return jsonify(query_table("mail"))

@app.route('/inventory')
def get_inventory():
    return jsonify(query_table("inventory"))

@app.route('/article')
def get_article():
    return jsonify(query_table("article"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
