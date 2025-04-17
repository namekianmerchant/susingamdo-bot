from flask import Flask, request, Response
import json

app = Flask(__name__)

sensitivity_table = {
    1: 195, 2: 98, 3: 65, 4: 49, 5: 39,
    6: 33, 7: 28, 8: 24, 9: 22, 10: 19
}

def get_recommended_sensitivity(converted_current):
    for sensitivity, min_current in sorted(sensitivity_table.items()):
        if converted_current >= min_current:
            return sensitivity
    return max(sensitivity_table.keys())

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.get_json()
        utterance = body.get("userRequest", {}).get("utterance", "")
        value = float(utterance)
        converted = round(value * 0.43, 2)
        recommended = get_recommended_sensitivity(converted)

        result_text = f"변환 전류: {converted} mA / 추천 감도: {recommended}"

        response_body = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": result_text
                        }
                    }
                ]
            }
        }

        return Response(
            json.dumps(response_body, ensure_ascii=False),
            status=200,
            content_type='application/json'
        )

    except Exception as e:
        error_response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "❗ 오류 발생: 숫자만 입력해주세요."
                        }
                    }
                ]
            }
        }

        return Response(
            json.dumps(error_response, ensure_ascii=False),
            status=200,
            content_type='application/json'
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
