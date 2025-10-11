"""
logging 라이브러리 자세한 설명
"""

import logging

# ============================================================
# 1. logging.basicConfig() - 로깅 기본 설정
# ============================================================

"""
logging.basicConfig(level=logging.INFO)

의미:
- "앞으로 logging을 사용할 때 기본 설정을 해줘!"
- level=logging.INFO → "INFO 레벨 이상만 보여줘"
"""

# 로그 레벨 5단계 (낮은 것부터 높은 것 순서)
print("=" * 60)
print("로그 레벨 5단계")
print("=" * 60)
print("""
1. DEBUG    (10) : 개발 중 디버깅용 상세 정보
2. INFO     (20) : 일반적인 정보 메시지  👈 우리가 설정한 레벨
3. WARNING  (30) : 경고 (문제는 아니지만 주의)
4. ERROR    (40) : 에러 발생
5. CRITICAL (50) : 치명적 에러 (프로그램 중단될 수도)
""")

# ============================================================
# 2. logger = logging.getLogger(__name__)
# ============================================================

"""
의미:
- "이 파일 전용 로거(logger)를 만들어줘!"
- __name__ : 파일 이름 (자동으로 들어감)

왜 getLogger(__name__)을 쓰나요?
→ 여러 파일에서 logging을 쓸 때, 어느 파일에서 찍힌 로그인지 알 수 있어요!
"""

# 예시: 파일명이 자동으로 들어감
logger = logging.getLogger(__name__)  # __name__ = "__main__" (직접 실행 시)

print("\n" + "=" * 60)
print("Logger 이름 확인")
print("=" * 60)
print(f"Logger 이름: {logger.name}")


# ============================================================
# 3. 실제 사용 예시
# ============================================================

print("\n" + "=" * 60)
print("로그 레벨별 출력 테스트")
print("=" * 60)

# 기본 설정: INFO 레벨
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("\n[현재 설정: level=INFO]")
print("INFO 이상만 출력됩니다.\n")

logger.debug("🔍 DEBUG: 변수 x = 10")           # ❌ 안 보임 (레벨이 낮아서)
logger.info("ℹ️  INFO: 파일 로딩 시작")          # ✅ 보임
logger.warning("⚠️  WARNING: 메모리 사용량 높음") # ✅ 보임
logger.error("❌ ERROR: 파일을 찾을 수 없음")     # ✅ 보임
logger.critical("🔥 CRITICAL: 시스템 다운!")     # ✅ 보임


# ============================================================
# 4. 레벨을 DEBUG로 바꾸면?
# ============================================================

print("\n" + "=" * 60)
print("레벨을 DEBUG로 변경")
print("=" * 60)

# 새로운 로거 생성 (레벨 변경을 위해)
logger2 = logging.getLogger("test_logger")
logger2.setLevel(logging.DEBUG)

# 핸들러 추가 (콘솔에 출력하기 위해)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger2.addHandler(handler)

print("\n[현재 설정: level=DEBUG]")
print("모든 레벨이 출력됩니다.\n")

logger2.debug("🔍 DEBUG: 변수 x = 10")           # ✅ 이제 보임!
logger2.info("ℹ️  INFO: 파일 로딩 시작")
logger2.warning("⚠️  WARNING: 메모리 사용량 높음")
logger2.error("❌ ERROR: 파일을 찾을 수 없음")
logger2.critical("🔥 CRITICAL: 시스템 다운!")


# ============================================================
# 5. 실무에서 자주 쓰는 패턴
# ============================================================

print("\n" + "=" * 60)
print("실무 활용 예시")
print("=" * 60)

# 패턴 1: 함수 시작/끝 로깅
def load_document(file_path):
    logger.info(f"문서 로딩 시작: {file_path}")
    
    # 실제 작업...
    
    logger.info(f"문서 로딩 완료: {file_path}")
    return "문서 내용"

# 패턴 2: 에러 처리
def divide(a, b):
    try:
        result = a / b
        logger.info(f"계산 성공: {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        logger.error(f"0으로 나눌 수 없습니다: {a} / {b}")
        return None

print("\n--- 함수 실행 ---")
load_document("sample.txt")
divide(10, 2)
divide(10, 0)  # 에러 발생


# ============================================================
# 6. 파일로 저장하기
# ============================================================

print("\n" + "=" * 60)
print("로그를 파일로 저장")
print("=" * 60)

# 파일 핸들러 설정
file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("테스트모듈/app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# 로그 포맷 설정
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
file_logger.addHandler(file_handler)

# 로그 기록
file_logger.info("이 로그는 app.log 파일에 저장됩니다")
file_logger.warning("경고 메시지도 저장됩니다")

print("✓ app.log 파일을 확인해보세요!")


# ============================================================
# 7. 우리 프로젝트에서 사용하는 이유
# ============================================================

print("\n" + "=" * 60)
print("우리 프로젝트에서 logging을 쓰는 이유")
print("=" * 60)

print("""
1. 디버깅이 쉬워져요
   - 어느 단계에서 문제가 생겼는지 추적 가능
   
2. 성능 모니터링
   - 파일 로딩: 2.5초
   - 임베딩 생성: 10.3초
   - 벡터 저장: 1.2초
   
3. 운영 중 문제 파악
   - 사용자가 "안 돼요"라고 하면
   - 로그 파일 보고 원인 찾기
   
4. print()보다 전문적
   - 배포 시 print()는 지저분
   - logger.debug()는 나중에 끌 수 있음
""")


# ============================================================
# 8. 요약 및 비교
# ============================================================

print("\n" + "=" * 60)
print("print vs logging 비교")
print("=" * 60)

print("""
개발 단계        | print()           | logging
---------------|-------------------|------------------
개발 중         | ✅ 간편함          | ✅ 체계적
디버깅          | ⚠️  일일이 지워야   | ✅ 레벨 조정만
배포 시         | ❌ 지저분함         | ✅ 깔끔함
문제 추적       | ❌ 기록 안 남음     | ✅ 파일로 저장
팀 협업         | ⚠️  통일성 없음     | ✅ 표준화
""")

print("\n결론: 작은 프로젝트는 print()도 OK, 큰 프로젝트는 logging 필수!")