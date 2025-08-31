from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI

# 커스텀 예외
class GPTServiceError(Exception):
    # GPT 호출 실패 등 외부 AI 서비스 관련 에러
    def __init__(self, message: str = "외부 AI 서비스 호출 실패"):
        self.message = message
        super().__init__(self.message)

# 애플리케이션 시작 시 한 번 호출해서 예외 핸들러들을 전역으로 등록
def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"status": 400, "message": str(exc)}
        )

    @app.exception_handler(GPTServiceError)
    async def gpt_service_error_handler(request: Request, exc: GPTServiceError):
        return JSONResponse(
            status_code=502,
            content={"status": 502, "message": exc.message}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "서버 내부 오류가 발생했습니다."}
        )