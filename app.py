import sqlitecloud
from flask import Flask, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_name = "sqlitegoldshoot0720.db"

@app.route('/')
def index():
    html = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <title>文章檔案顯示</title>
</head>
<body>
  <h2>從 /article 取得檔案並顯示</h2>
  <div id="viewer">載入中...</div>

  <script>
    fetch("/article")
      .then(res => res.json())
      .then(data => {
        if (!data.length) {
          document.getElementById("viewer").textContent = "沒有資料";
          return;
        }
        const firstRecord = data[0];
        const base64Str = firstRecord.img1;  // base64 字串欄位名稱
        // 假設有 file1type 或 type 欄位，依實際資料調整
        const fileType = firstRecord.file1type || firstRecord.type || "png";
        const viewer = document.getElementById("viewer");
        let mimeType = "";

        switch(fileType.toLowerCase()) {
          case "png":
          case "jpg":
          case "jpeg":
            mimeType = `image/${fileType}`;
            viewer.innerHTML = `<img src="data:${mimeType};base64,${base64Str}" style="max-width:100%;">`;
            break;
          case "pdf":
            mimeType = "application/pdf";
            viewer.innerHTML = `<embed src="data:${mimeType};base64,${base64Str}" width="100%" height="600px">`;
            break;
          case "mp4":
            mimeType = "video/mp4";
            viewer.innerHTML = \`
              <video controls width="100%" height="auto">
                <source src="data:${mimeType};base64,${base64Str}" type="${mimeType}">
                您的瀏覽器不支援影片播放。
              </video>\`;
            break;
          default:
            viewer.textContent = "不支援的檔案類型：" + fileType;
        }
      })
      .catch(err => {
        console.error("載入錯誤:", err);
        document.getElementById("viewer").textContent = "載入失敗";
      });
  </script>
</body>
</html>
"""
    return Response(html, mimetype="text/html")

@app.route('/subscription')
def get_subscription():
    conn = sqlitecloud.connect(
        "sqlitecloud://cmk0dgzqhk.g2.sqlite.cloud:8860/auth.sqlitecloud?apikey=tFponRnK20mvO37gEImnuRCuVLDFvydAbbopxaVkXPg"
    )
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.execute("SELECT * FROM subscription")
    
    # 取得欄位名稱
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # 轉為 list of dicts
    result = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/mail')
def get_mail():
    conn = sqlitecloud.connect(
        "sqlitecloud://cmk0dgzqhk.g2.sqlite.cloud:8860/auth.sqlitecloud?apikey=tFponRnK20mvO37gEImnuRCuVLDFvydAbbopxaVkXPg"
    )
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.execute("SELECT * FROM mail")
    
    # 取得欄位名稱
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # 轉為 list of dicts
    result = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/inventory')
def get_inventory():
    conn = sqlitecloud.connect(
        "sqlitecloud://cmk0dgzqhk.g2.sqlite.cloud:8860/auth.sqlitecloud?apikey=tFponRnK20mvO37gEImnuRCuVLDFvydAbbopxaVkXPg"
    )
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.execute("SELECT * FROM inventory")
    
    # 取得欄位名稱
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    # 轉為 list of dicts，img1 原本就是 Base64 字串，直接回傳
    result = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(result)

@app.route('/article')
def get_article():
    conn = sqlitecloud.connect(
        "sqlitecloud://cmk0dgzqhk.g2.sqlite.cloud:8860/auth.sqlitecloud?apikey=tFponRnK20mvO37gEImnuRCuVLDFvydAbbopxaVkXPg"
    )
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.execute("SELECT * FROM article")
    
    # 取得欄位名稱
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    # 轉為 list of dicts，img1 原本就是 Base64 字串，直接回傳
    result = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
