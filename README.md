# 반달곰 커피 지점 찾기 프로젝트

## 📋 프로젝트 개요
코디세이 AI 올인원 프로그램을 위한 데이터 분석 및 시각화 프로젝트입니다.
3단계 파이프라인을 통해 CSV 데이터를 처리하고, 지도를 시각화하며, BFS 알고리즘으로 최단경로를 찾습니다.

## 🎯 완성된 기능
✅ **1단계**: pandas를 이용한 CSV 데이터 처리 및 병합  
✅ **2단계**: matplotlib를 이용한 지도 시각화  
✅ **3단계**: BFS 알고리즘을 이용한 최단경로 탐색  
✅ **웹 대시보드**: Streamlit을 이용한 교육용 인터페이스  
✅ **5색깔 코딩 시스템**: 코드 이해를 돕는 색깔별 주석  
✅ **한글 주석**: 모든 코드에 한국어 설명 추가  
✅ **요점정리 박스**: 각 단계별 학습 내용 정리  

## 🚀 실행 방법

### Streamlit 웹 앱 실행
```bash
streamlit run app.py --server.port 5000
```

### 개별 단계 실행
```bash
# 1단계: 데이터 처리
python caffee_map_final.py

# 2단계: 지도 시각화  
python map_draw_real.py

# 3단계: 최단경로 탐색
python map_direct_save.py
```

## 📁 파일 구조
```
프로젝트/
├── app.py                 # Streamlit 웹 대시보드 (메인)
├── caffee_map_final.py    # 1단계: 데이터 처리
├── map_draw_real.py       # 2단계: 지도 시각화
├── map_direct_save.py     # 3단계: 최단경로 탐색
├── area_map.csv           # 좌표 데이터
├── area_struct.csv        # 구조물 데이터
├── area_category.csv      # 카테고리 데이터
├── map.png               # 생성된 지도
├── map_final.png         # 최단경로가 표시된 지도
└── home_to_cafe.csv      # 최단경로 좌표
```

## 🔧 기술 스택
- **Python 3.11**
- **pandas**: 데이터 처리 및 분석
- **matplotlib**: 데이터 시각화
- **streamlit**: 웹 애플리케이션 프레임워크
- **BFS 알고리즘**: 최단경로 탐색

## 📊 데이터 소스
- **좌표계**: X축(1~7), Y축(1~8)
- **구조물 종류**: 아파트, 빌딩, 반달곰커피, 마이홈, 건설현장
- **지역**: area 1 데이터만 사용

## 🎓 교육적 특징
- **5색깔 코딩**: 초기화(파란색), 반복문(초록색), 조건문(빨간색), 경로확장(보라색), 데이터변환(주황색)
- **단계별 학습**: 기초 → 상세 → 심화 설명
- **실무 연결**: 각 기술의 실제 활용 예시 제공
- **한글 주석**: 영어 코드에 한국어 설명 병행

## 📈 프로젝트 성과
- 완전한 3단계 데이터 파이프라인 구현
- 실제 CSV 데이터를 사용한 현실적인 분석
- 교육용 웹 인터페이스로 학습 효과 극대화
- PEP 8 준수한 깔끔한 코드 구조

---
**개발자**: 코디세이 AI 올인원 프로그램  
**완성일**: 2025년 7월 23일