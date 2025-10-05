#!/usr/bin/env python3
"""
실제 노동법 데이터 크롤링 스크립트 (참고용)
주의: 실행 전 각 사이트의 robots.txt와 이용약관을 확인하세요.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time


def crawl_labor_law():
    """
    국가법령정보센터에서 근로기준법 전문 가져오기
    
    실제로는 API를 사용하거나 수동으로 복사하는 것을 권장합니다.
    여기서는 예시 코드만 제공합니다.
    """
    print("⚠️  실제 크롤링 예시 (실행 안 함)")
    print("근로기준법: https://www.law.go.kr 에서 수동 복사 권장")
    
    # 예시 URL (실제로는 변경될 수 있음)
    # url = "https://www.law.go.kr/법령/근로기준법"
    
    sample_note = """
    # 실제 수집 방법 (권장)
    
    1. 국가법령정보센터 접속
       https://www.law.go.kr
    
    2. 검색창에 "근로기준법" 입력
    
    3. 법령 전체보기 → 복사 → 텍스트 파일로 저장
       data/raw/laws/근로기준법.txt
    
    4. 추가로 필요한 법률:
       - 최저임금법
       - 근로자퇴직급여보장법
       - 남녀고용평등법
    """
    
    output_path = Path("data/raw/laws/크롤링안내.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sample_note)
    
    print(f"✓ 안내 파일 생성: {output_path}")


def crawl_moel_faq():
    """
    고용노동부 FAQ 크롤링
    
    실제 사이트 구조에 맞춰 수정 필요
    """
    print("\n⚠️  고용노동부 FAQ 크롤링 예시")
    
    # 예시 코드 (실제 사이트 구조는 다를 수 있음)
    sample_code = """
    # 실제 크롤링 예시 코드
    
    def fetch_faq_from_moel():
        base_url = "https://www.moel.go.kr"
        # 고용노동부 FAQ 페이지
        faq_url = f"{base_url}/faq/faqList.do"
        
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        
        response = requests.get(faq_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 실제 구조에 맞춰 셀렉터 수정 필요
        faq_items = soup.select('.faq-item')
        
        faqs = []
        for item in faq_items:
            question = item.select_one('.question').text.strip()
            answer = item.select_one('.answer').text.strip()
            faqs.append({
                'question': question,
                'answer': answer
            })
        
        return faqs
    
    # 주의사항:
    # 1. 너무 빠른 요청은 서버에 부담 (time.sleep 사용)
    # 2. robots.txt 확인 필수
    # 3. 가능하면 공식 API 사용
    """
    
    output_path = Path("data/raw/faqs/크롤링가이드.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sample_code)
    
    print(f"✓ 가이드 파일 생성: {output_path}")


def crawl_court_cases():
    """
    대법원 종합법률정보 판례 크롤링
    
    주의: 대법원 사이트는 공식 API가 있을 수 있음
    """
    print("\n⚠️  판례 수집 가이드")
    
    guide = """
    # 판례 수집 방법
    
    ## 1. 대법원 종합법률정보 이용
    https://glaw.scourt.go.kr
    
    - 검색어: "근로기준법", "부당해고", "임금체불" 등
    - 판례 유형: 민사, 행정
    - 기간: 최근 5년
    
    ## 2. 판례 선별 기준
    - 대법원 판결 우선 (확정된 법리)
    - 실무에 자주 적용되는 사례
    - 명확한 판시사항이 있는 경우
    
    ## 3. 저장 형식
    각 판례를 다음 구조로 저장:
    
    ```
    # 사건명: [법원명] [사건번호]
    
    ## 쟁점
    [핵심 쟁점]
    
    ## 사실관계
    [사건 개요]
    
    ## 판결 요지
    [법원의 판단]
    
    ## 관련 법조항
    [적용된 법률]
    ```
    
    ## 4. 저작권 주의
    - 판례는 공공저작물이지만, 출처를 명시해야 함
    - 상업적 이용 시 별도 확인 필요
    """
    
    output_path = Path("data/raw/cases/판례수집가이드.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(guide)
    
    print(f"✓ 가이드 파일 생성: {output_path}")


def download_with_api():
    """
    공식 API 사용 예시
    
    일부 사이트는 Open API를 제공합니다.
    """
    print("\n📌 공식 API 활용 팁")
    
    api_guide = """
    # 공식 API 활용하기
    
    ## 1. 법제처 Open API
    https://www.law.go.kr/DRF/lawService.do
    
    - API Key 발급 필요 (무료)
    - 법령 정보를 XML/JSON으로 제공
    - 사용 예시:
    
    ```python
    import requests
    
    api_key = "YOUR_API_KEY"
    url = "http://www.law.go.kr/DRF/lawService.do"
    
    params = {
        'OC': api_key,
        'target': 'law',
        'MST': '근로기준법',
        'type': 'XML'
    }
    
    response = requests.get(url, params=params)
    # XML 파싱 후 저장
    ```
    
    ## 2. 고용노동부 Open API
    https://www.data.go.kr
    
    - 공공데이터포털에서 검색: "고용노동부"
    - 다양한 통계 및 정보 제공
    
    ## 3. API 사용 시 장점
    - 안정적인 데이터 제공
    - 법적 문제 없음
    - 최신 정보 보장
    """
    
    output_path = Path("data/raw/API활용가이드.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(api_guide)
    
    print(f"✓ API 가이드 생성: {output_path}")


def main():
    """메인 함수"""
    print("=" * 60)
    print("실제 데이터 크롤링 가이드 (참고용)")
    print("=" * 60)
    
    print("\n⚠️  주의사항:")
    print("1. 각 사이트의 robots.txt 확인")
    print("2. 이용약관 준수")
    print("3. 가능하면 공식 API 사용")
    print("4. 크롤링 시 적절한 딜레이 (time.sleep) 사용")
    print("5. 저작권 및 출처 표시")
    
    print("\n" + "-" * 60)
    
    # 각 가이드 파일 생성
    crawl_labor_law()
    crawl_moel_faq()
    crawl_court_cases()
    download_with_api()
    
    print("\n" + "=" * 60)
    print("✅ 크롤링 가이드 생성 완료")
    print("=" * 60)
    
    print("\n현재 상태:")
    print("✓ 샘플 데이터 준비 완료 (Step 2 완료)")
    print("→ 다음: Step 3 (문서 로더 개발)")
    
    print("\n실제 데이터 수집은 나중에:")
    print("- 프로토타입 완성 후")
    print("- 샘플 데이터로 먼저 전체 파이프라인 검증")
    print("- 필요 시 수동 복사도 가능")


if __name__ == "__main__":
    main()