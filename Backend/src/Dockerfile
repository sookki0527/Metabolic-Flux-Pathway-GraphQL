# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉토리
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
COPY . .

# 의존성 설치
RUN pip install -r requirements.txt

# 포트 설정 (Railway는 ${PORT}로 설정)
EXPOSE 8000

# 실행 커맨드
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
