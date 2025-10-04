#!/usr/bin/env python3
"""
프로젝트 디렉토리 구조 자동 생성 스크립트
"""

import os
from pathlib import Path

def create_project_structure():
    """프로젝트 폴더 구조 생성"""
    
    # 생성할 디렉토리 목록
    directories = [
        "data/raw/laws",
        "data/raw/faqs",
        "data/raw/cases",
        "data/processed",
        "models",
        "agents",
        "tools",
        "config",
        "logs",
        "tests",
    ]
    
    # __init__.py가 필요한 패키지 디렉토리
    package_dirs = ["agents", "tools", "config"]
    
    # 디렉토리 생성
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}/")
    
    # __init__.py 파일 생성
    for pkg_dir in package_dirs:
        init_file = Path(pkg_dir) / "__init__.py"
        init_file.touch(exist_ok=True)
        print(f"✓ Created: {init_file}")
    
    # .gitignore 생성
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
*.so
.Python
.env
.gitignore

# 데이터
data/processed/*
!data/processed/.gitkeep
models/*
!models/.gitkeep

# 로그
logs/*
!logs/.gitkeep

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("✓ Created: .gitignore")
    
    # .gitkeep 파일 생성 (빈 폴더를 Git에 추가하기 위함)
    gitkeep_dirs = ["data/processed", "models", "logs"]
    for directory in gitkeep_dirs:
        gitkeep_file = Path(directory) / ".gitkeep"
        gitkeep_file.touch(exist_ok=True)
    
    print("\n✅ 프로젝트 구조 생성 완료!")
    print("\n다음 단계:")
    print("1. pip install -r requirements.txt")
    print("2. cp .env.example .env")
    print("3. Ollama 설치 및 모델 다운로드")
    print("4. Weaviate Docker 실행")

if __name__ == "__main__":
    create_project_structure()