# 데이터를 프론트엔드 공통 성공 응답 형식으로 감싸며 업무 메시지를 지정할 수 있습니다.
def ok(data, result_message: str = "SUCCESS"):
    return {"result": "SUCCESS", "resultMessage": result_message, "data": data}
