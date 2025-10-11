"""
프로젝트 전역 로깅 설정 모듈

사용법:
    from config.logging_config import get_logger
    
    logger = get_logger(__name__)
    logger.info("로그 메시지")
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# 로그 폴더 설정
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 로거 생성 함수
def get_logger(
    name: str,
    level: int = logging.INFO,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_to_file: bool = True
) -> logging.Logger:
    """
    설정된 로거 반환
    
    Args:
        name: 로거 이름 (보통 __name__ 사용)
        level: 로거 전체 레벨
        console_level: 콘솔 출력 레벨
        file_level: 파일 저장 레벨
        log_to_file: 파일 저장 여부
        
    Returns:
        설정된 Logger 객체
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("테스트")
        2025-10-11 14:30:25 - __main__ - INFO - 테스트
    """
    
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 이미 핸들러가 있으면 중복 방지
    if logger.handlers:
        return logger
    
    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. 파일 핸들러
    if log_to_file:
        # 로그 파일명: 모듈명_날짜시간.log
        module_name = name.split('.')[-1]  # 'tools.document_loader' → 'document_loader'
        log_filename = LOG_DIR / f"{module_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.debug(f"로그 파일: {log_filename}")
    
    return logger

# 간단 버전 (기본 설정)
def setup_logger(name: str) -> logging.Logger:
    """
    기본 설정으로 로거 생성 (간단 버전)
    
    Args:
        name: 로거 이름
        
    Returns:
        Logger 객체
        
    Example:
        >>> from config.logging_config import setup_logger
        >>> logger = setup_logger(__name__)
    """
    return get_logger(
        name=name,
        level=logging.DEBUG,
        console_level=logging.INFO,
        file_level=logging.DEBUG,
        log_to_file=True
    )

# 프로젝트 전체 로거 (선택사항)
def get_project_logger() -> logging.Logger:
    """
    프로젝트 전체 공통 로거
    
    모든 모듈에서 같은 로그 파일 사용하고 싶을 때
    
    Returns:
        공통 Logger
    """
    log_filename = LOG_DIR / f"project_{datetime.now().strftime('%Y%m%d')}.log"
    
    logger = logging.getLogger("labor_law_chatbot")
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    # 파일 (하루치)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# 로깅 레벨 설정 헬퍼
class LogLevel:
    """로깅 레벨 상수"""
    DEBUG = logging.DEBUG      # 10
    INFO = logging.INFO        # 20
    WARNING = logging.WARNING  # 30
    ERROR = logging.ERROR      # 40
    CRITICAL = logging.CRITICAL # 50

if __name__ == "__main__":
    print("=" * 70)
    print("로깅 설정 모듈 테스트")
    print("=" * 70)
    
    # 예시 1: 기본 로거
    print("\n[예시 1] 기본 로거")
    print("-" * 70)
    
    logger1 = setup_logger(__name__)
    
    logger1.debug("디버그 메시지 (파일에만)")
    logger1.info("정보 메시지 (콘솔+파일)")
    logger1.warning("경고 메시지")
    logger1.error("에러 메시지")
    
    # 예시 2: 커스텀 설정
    print("\n[예시 2] 커스텀 로거 (콘솔 WARNING 이상만)")
    print("-" * 70)
    
    logger2 = get_logger(
        name="custom_logger",
        console_level=logging.WARNING,  # 콘솔은 WARNING부터
        file_level=logging.DEBUG        # 파일은 DEBUG부터
    )
    
    logger2.debug("이건 파일에만")
    logger2.info("이것도 파일에만")
    logger2.warning("이건 콘솔+파일 둘 다")
    logger2.error("이것도 콘솔+파일")
    
    # 예시 3: 프로젝트 공통 로거
    print("\n[예시 3] 프로젝트 공통 로거")
    print("-" * 70)
    
    project_logger = get_project_logger()
    project_logger.info("프로젝트 전체 로그")
    
    # 결과 확인
    print("\n" + "=" * 70)
    print("✅ 테스트 완료!")
    print("=" * 70)
    print(f"\n생성된 로그 파일:")
    print(f"  logs/ 폴더 확인")
    
    import os
    if os.path.exists("logs"):
        for log_file in Path("logs").glob("*.log"):
            print(f"    - {log_file.name}")