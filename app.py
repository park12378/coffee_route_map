"""
Streamlit 웹 애플리케이션: 반달곰 커피 프로젝트 대시보드
"""

import streamlit as st
import pandas as pd
import os
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="반달곰 커피 프로젝트",
    page_icon="☕",
    layout="wide"
)

# 제목
st.title("☕ 반달곰 커피 찾기 프로젝트")
st.markdown("**코디세이 AI 올인원 프로그램** - 데이터 분석 및 경로 탐색")

# 사이드바 메뉴
st.sidebar.title("🗺 프로젝트 단계")
stage = st.sidebar.selectbox(
    "단계를 선택하세요:",
    ["프로젝트 소개", "1단계: 데이터 분석", "2단계: 지도 시각화", "3단계: 최단경로 탐색"]
)

# 각 단계별 내용
if stage == "프로젝트 소개":
    st.header("📋 프로젝트 개요")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 프로젝트 목표
        이 프로젝트는 **3단계 파이프라인**으로 구성된 데이터 분석 및 경로 탐색 시스템입니다.
        
        ### 📊 사용 데이터
        - **area_map.csv**: 좌표 및 건설현장 정보
        - **area_struct.csv**: 구조물 카테고리 및 지역 정보  
        - **area_category.csv**: 구조물 이름 매핑
        
        ### 🔧 기술 스택
        - **Python**: 메인 프로그래밍 언어
        - **Pandas**: 데이터 처리 및 분석
        - **Matplotlib**: 지도 시각화
        - **BFS 알고리즘**: 최단경로 탐색
        
        ### 📈 3단계 프로세스
        1. **데이터 분석**: CSV 파일 병합 및 전처리
        2. **지도 시각화**: Matplotlib를 이용한 시각적 지도 생성
        3. **경로 탐색**: BFS 알고리즘으로 최단경로 계산
        """)
    
    with col2:
        st.subheader("🏗 구조물 종류")
        st.markdown("""
        - 🏠 아파트 (갈색 원)
        - 🏢 빌딩 (갈색 원)
        - ☕ 반달곰커피 (녹색 사각형)
        - 🚧 건설현장 (회색 사각형)
        """)

elif stage == "1단계: 데이터 분석":
    st.header("📊 1단계: 데이터 분석")
    
    # 데이터 처리 원리 설명
    st.subheader("🧠 데이터 처리 원리")
    
    with st.expander("📚 pandas 데이터 처리 과정 이해하기", expanded=False):
        col_explain1, col_explain2 = st.columns(2)
        
        with col_explain1:
            st.markdown("""
            **🔍 pandas 란?**
            - **데이터 분석 라이브러리**: CSV, Excel 등 다양한 데이터 파일 처리 → `pd.read_csv()`
            - **DataFrame**: 표 형태의 데이터 구조 (행과 열) → `df`
            - **데이터 병합**: 여러 파일을 하나로 합치기 → `merge()`
            
            **🗂 파일 구조**
            - area_map.csv: 좌표와 건설현장 정보 → `(x, y, ConstructionSite)`
            - area_struct.csv: 구조물 종류와 구역 → `(category, area)`
            - area_category.csv: 숫자를 이름으로 변환 → `{1: 'Apartment'}`
            """)
        
        with col_explain2:
            st.markdown("""
            **⚙️ 처리 과정**
            1. **<span style='color: #1976d2; font-weight: bold;'>파일 읽기</span>**: 3개 CSV 파일을 각각 DataFrame으로 변환 → `pd.read_csv()` **<span style='color: #1976d2;'>(초기화)</span>**
            2. **<span style='color: #f57c00; font-weight: bold;'>데이터 정리</span>**: 공백 제거, 컬럼명 정리 → `str.strip()` **<span style='color: #f57c00;'>(데이터 변환)</span>**
            3. **<span style='color: #7b1fa2; font-weight: bold;'>병합하기</span>**: x, y 좌표를 기준으로 파일들 합치기 → `merge(on=['x', 'y'])` **<span style='color: #7b1fa2;'>(데이터 병합)</span>**
            4. **<span style='color: #d32f2f; font-weight: bold;'>필터링</span>**: area 1 지역만 추출 → `df[df['area'] == 1]` **<span style='color: #d32f2f;'>(조건 체크)</span>**
            
            **📊 결과**
            - 통합된 하나의 데이터셋 생성 → `merged_data`
            - 반달곰 커피 지역(area 1)만 분리 → `filtered_data`
            - 구조물 정보와 좌표 정보 연결 완료 → `ready_for_mapping`
            """, unsafe_allow_html=True)
    
    with st.expander("💻 핵심 데이터 처리 코드 보기", expanded=False):
        st.markdown("**🔧 pandas 데이터 처리 핵심 코드**")
        
        # 주석을 별도로 강조해서 표시
        st.markdown("**📝 핵심 로직 설명:**")
        st.markdown("""
        - **<span style='color: #1976d2; font-weight: bold;'>파일 읽기</span>**: CSV 파일을 DataFrame으로 변환 **<span style='color: #1976d2;'>(초기화)</span>**
        - **<span style='color: #f57c00; font-weight: bold;'>데이터 정리</span>**: 공백과 특수문자 제거 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - **<span style='color: #7b1fa2; font-weight: bold;'>병합 작업</span>**: 공통 컬럼(x, y)으로 데이터 합치기 **<span style='color: #7b1fa2;'>(데이터 병합)</span>**
        - **<span style='color: #d32f2f; font-weight: bold;'>필터링</span>**: 조건에 맞는 데이터만 추출 **<span style='color: #d32f2f;'>(조건 체크)</span>**
        - **<span style='color: #f57c00; font-weight: bold;'>컬럼 매핑</span>**: 숫자 코드를 실제 이름으로 변환 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - **<span style='color: #f57c00; font-weight: bold;'>결과 저장</span>**: 처리된 데이터를 새 파일로 저장 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        """, unsafe_allow_html=True)
        
        st.markdown("**💻 실제 코드 (주석 포함):**")
        
        # 주석을 굵은 색깔로 강조해서 표시
        st.markdown("**🎨 주석 색깔 의미:**")
        col_legend1, col_legend2, col_legend3 = st.columns(3)
        
        with col_legend1:
            st.markdown("""
            <span style="color:blue; font-weight:bold;">🔵 파란색</span> = 초기화 관련
            <span style="color:green; font-weight:bold;">🟢 초록색</span> = 반복문/루프
            """, unsafe_allow_html=True)
        
        with col_legend2:
            st.markdown("""
            <span style="color:red; font-weight:bold;">🔴 빨간색</span> = 조건 체크
            <span style="color:purple; font-weight:bold;">🟣 보라색</span> = 데이터 병합
            """, unsafe_allow_html=True)
        
        with col_legend3:
            st.markdown("""
            <span style="color:orange; font-weight:bold;">🟠 주황색</span> = 데이터 변환
            """, unsafe_allow_html=True)
        
        st.markdown("**🔍 라인별 주석 설명:**")
        col_comment1, col_comment2 = st.columns(2)
        
        with col_comment1:
            st.markdown("""
            **파일 읽기 부분:**
            - `pd.read_csv('area_map.csv')` <span style="color:blue; font-weight:bold;">← CSV 파일을 DataFrame으로 읽기</span>
            - `pd.read_csv('area_struct.csv')` <span style="color:blue; font-weight:bold;">← 구조물 정보 파일 읽기</span>
            - `pd.read_csv('area_category.csv')` <span style="color:blue; font-weight:bold;">← 카테고리 정보 파일 읽기</span>
            
            **데이터 정리:**
            - `columns.str.strip()` <span style="color:orange; font-weight:bold;">← 컬럼명 공백 제거</span>
            - `['struct'].str.strip()` <span style="color:orange; font-weight:bold;">← 데이터 공백 제거</span>
            """, unsafe_allow_html=True)
        
        with col_comment2:
            st.markdown("""
            **병합 작업:**
            - `area_map.merge(area_struct)` <span style="color:purple; font-weight:bold;">← 지도와 구조물 데이터 병합</span>
            - `merged_data.merge(area_category)` <span style="color:purple; font-weight:bold;">← 카테고리 이름 추가</span>
            - `on=['x', 'y']` <span style="color:purple; font-weight:bold;">← x, y 좌표 기준으로 병합</span>
            
            **필터링:**
            - `merged_data[merged_data['area'] == 1]` <span style="color:red; font-weight:bold;">← area 1만 필터링</span>
            - `len(filtered_data)` <span style="color:orange; font-weight:bold;">← 필터링된 데이터 개수 확인</span>
            """, unsafe_allow_html=True)
        
        # 주석을 더 강조해서 보여주기
        st.info("🟡 **파일 읽기** → `pd.read_csv()`: 컴퓨터에 저장된 CSV 파일을 pandas가 이해할 수 있는 표 형태로 변환                                    (초기화)")
        st.code("area_map = pd.read_csv('area_map.csv')  # 지도데이터 = CSV파일읽기", language='python')
        
        st.info("🟡 **데이터 정리** → `str.strip()`: 데이터에 들어있는 불필요한 공백 제거해서 깔끔하게 만들기                                    (데이터 변환)")
        st.code("area_category['struct'] = area_category['struct'].str.strip()  # 구조물명 = 공백제거", language='python')
        
        st.info("🟡 **데이터 병합** → `merge()`: 공통된 컬럼(x, y)을 기준으로 여러 파일의 정보를 하나로 합치기                                    (데이터 병합)")
        st.code("merged_data = area_map.merge(area_struct, on=['x', 'y'])  # 병합데이터 = 지도 + 구조물", language='python')
        
        st.info("🟡 **조건 필터링** → `df[조건]`: 전체 데이터에서 특정 조건을 만족하는 행들만 골라내기                                    (조건 체크)")
        st.code("filtered_data = merged_data[merged_data['area'] == 1]  # 필터데이터 = area가 1인 것만", language='python')
        
        st.info("🟡 **컬럼 매핑** → `map()`: 숫자 코드(1, 2, 3, 4)를 실제 이름(아파트, 빌딩 등)으로 바꾸기                                    (데이터 변환)")
        st.code("merged_data['struct'] = merged_data['category'].map(category_dict)", language='python')
        
        st.info("🟡 **결과 확인** → `len()`: 처리된 데이터의 개수를 세어서 올바르게 처리되었는지 확인                                    (데이터 변환)")
        st.code("print(f'area 1 데이터 크기: {len(filtered_data)}개')", language='python')
    
    with st.expander("📖 데이터 처리 용어 설명", expanded=False):
        st.markdown("**💡 코드에서 사용된 주요 용어들**")
        
        col_term1, col_term2 = st.columns(2)
        
        with col_term1:
            st.markdown("""
            **📦 pandas 관련**
            - <span style='color: #1976d2; font-weight: bold;'>DataFrame</span>: 표(행과 열) 형태의 데이터 구조 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>read_csv()</span>: CSV 파일을 DataFrame으로 읽어오는 함수 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>merge()</span>: 두 DataFrame을 공통 컬럼 기준으로 합치기 **<span style='color: #7b1fa2;'>(데이터 병합)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>columns</span>: DataFrame의 컬럼(열) 이름들 **<span style='color: #1976d2;'>(초기화)</span>**
            
            **🔄 데이터 조작**
            - <span style='color: #f57c00; font-weight: bold;'>str.strip()</span>: 문자열 양쪽 공백 제거 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>map()</span>: 값을 다른 값으로 매핑(변환) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #d32f2f; font-weight: bold;'>filter</span>: 조건에 맞는 데이터만 선택 **<span style='color: #d32f2f;'>(조건 체크)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>len()</span>: 데이터의 개수 세기 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            """, unsafe_allow_html=True)
        
        with col_term2:
            st.markdown("""
            **📍 프로젝트 관련**
            - <span style='color: #f57c00; font-weight: bold;'>area</span>: 지역 구분 번호 (1이 반달곰 커피 지역) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>category</span>: 구조물 종류를 나타내는 숫자 코드 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>struct</span>: category의 실제 이름 (Apartment, Building 등) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #d32f2f; font-weight: bold;'>ConstructionSite</span>: 건설현장 여부 (0=없음, 1=있음) **<span style='color: #d32f2f;'>(조건 체크)</span>**
            
            **⚙️ 파일 관련**
            - <span style='color: #1976d2; font-weight: bold;'>CSV</span>: Comma-Separated Values (쉼표로 구분된 값들) **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>x, y</span>: 2차원 좌표계의 가로, 세로 위치 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>on=['x', 'y']</span>: x와 y 컬럼을 기준으로 병합한다는 뜻 **<span style='color: #7b1fa2;'>(데이터 병합)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>merged_data</span>: 병합된 최종 데이터 **<span style='color: #7b1fa2;'>(데이터 병합)</span>**
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **🎯 핵심 개념**
        - <span style='color: #388e3c; font-weight: bold;'>iterrows()</span>: DataFrame을 한 줄씩 반복해서 처리 **<span style='color: #388e3c;'>(반복문)</span>**
        - <span style='color: #f57c00; font-weight: bold;'>NaN</span>: Not a Number (빈 값, 없는 데이터) **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - <span style='color: #388e3c; font-weight: bold;'>groupby()</span>: 특정 컬럼 값에 따라 데이터를 그룹으로 나누기 **<span style='color: #388e3c;'>(반복문)</span>**
        - <span style='color: #1976d2; font-weight: bold;'>index</span>: DataFrame에서 각 행을 구분하는 번호 **<span style='color: #1976d2;'>(초기화)</span>**
        """, unsafe_allow_html=True)
    
    # 데이터 불러오기
    try:
        area_map = pd.read_csv('area_map.csv')
        area_struct = pd.read_csv('area_struct.csv')
        area_category = pd.read_csv('area_category.csv')
        
        # 컬럼명과 데이터의 공백 제거
        area_category.columns = area_category.columns.str.strip()
        area_category['struct'] = area_category['struct'].str.strip()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🗺 area_map.csv")
            st.dataframe(area_map, height=300)
            st.caption(f"총 {len(area_map)}개 좌표 (전체 표시)")
        
        with col2:
            st.subheader("🏗 area_struct.csv")
            st.dataframe(area_struct, height=300)
            st.caption(f"총 {len(area_struct)}개 구조물 (전체 표시)")
        
        with col3:
            st.subheader("📋 area_category.csv")
            st.dataframe(area_category)
            st.caption(f"총 {len(area_category)}개 카테고리")
        
        # 병합된 데이터 표시
        st.subheader("🔗 병합된 데이터 (전체)")
        
        # 데이터 병합 과정 재현
        merged_data = area_map.merge(area_struct, on=['x', 'y'], how='left')
        st.dataframe(merged_data, height=400)
        st.caption(f"전체 데이터: {len(merged_data)}개 행 (225개 좌표 전체)")
        
        # area 1 데이터만 따로 표시
        st.subheader("🔗 area 1 데이터")
        area_1_data = merged_data[merged_data['area'] == 1].copy()
        st.dataframe(area_1_data)
        st.caption(f"area 1 데이터: {len(area_1_data)}개 행")
        
        # 구조물별 통계
        st.subheader("📈 구조물별 통계")
        structures = area_1_data[area_1_data['category'] != 0]
        if not structures.empty:
            # 카테고리 매핑
            category_mapping = area_category.set_index('category')['struct'].to_dict()
            
            structure_stats = structures.groupby('category').agg({
                'x': 'count',
                'area': 'first'
            }).rename(columns={'x': '개수', 'area': '지역'})
            
            structure_stats['구조물명'] = structure_stats.index.map(category_mapping)
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(structure_stats[['구조물명', '개수', '지역']])
            
            with col2:
                st.subheader("📍 구조물 위치")
                for category in structures['category'].unique():
                    struct_name = category_mapping.get(category, f'Category_{category}')
                    struct_locations = structures[structures['category'] == category][['x', 'y']]
                    locations = list(zip(struct_locations['x'], struct_locations['y']))
                    st.write(f"**{struct_name}**: {locations}")
        
    except FileNotFoundError as e:
        st.error(f"파일을 찾을 수 없습니다: {e}")
    
    # 1단계 요점정리 박스 추가
    st.markdown("---")
    st.subheader("📝 1단계 요점정리")
    
    col_summary1, col_summary2 = st.columns(2)
    
    with col_summary1:
        st.success("""
**🎯 핵심 배운 내용**

✅ pandas로 CSV 파일 읽기

✅ 데이터 병합(merge)

✅ 조건 필터링

✅ 데이터 정리

✅ 컬럼 매핑
        """)
    
    with col_summary2:
        st.info("""
**💡 실무에서 활용 가능한 기술**

🔹 Excel 대신 pandas

🔹 자동화 반복 작업

🔹 데이터 품질 관리

🔹 보고서 생성

🔹 다른 분야 응용
        """)

elif stage == "2단계: 지도 시각화":
    st.header("🗺 2단계: 지도 시각화")
    
    # 시각화 원리 설명
    st.subheader("🧠 matplotlib 시각화 원리")
    
    with st.expander("📚 matplotlib로 지도 그리기 과정 이해하기", expanded=False):
        col_explain1, col_explain2 = st.columns(2)
        
        with col_explain1:
            st.markdown("""
            **🔍 matplotlib 란?**
            - **그래프 라이브러리**: 차트, 그래프, 지도 등 시각화 도구 → `plt.plot()`
            - **Figure & Axes**: 캔버스(figure)와 그림 영역(axes) → `plt.subplots()`
            - **좌표계**: x, y 축을 이용한 2차원 평면 그리기 → `plt.xlim(), plt.ylim()`
            
            **🎨 그리기 요소**
            - Circle: 원 그리기 (아파트, 빌딩용) → `Circle(center, radius)`
            - Rectangle: 사각형 그리기 (커피숍, 건설현장용) → `Rectangle(position, width, height)`
            - patches: 도형들을 그림에 추가 → `ax.add_patch()`
            """)
        
        with col_explain2:
            st.markdown("""
            **⚙️ 그리기 과정**
            1. **<span style='color: #1976d2; font-weight: bold;'>캔버스 준비</span>**: 그림을 그릴 도화지 만들기 → `plt.subplots(figsize=(8, 6))` **<span style='color: #1976d2;'>(초기화)</span>**
            2. **<span style='color: #1976d2; font-weight: bold;'>좌표 설정</span>**: x, y 범위와 격자 표시 → `plt.xlim(0.5, 7.5)` **<span style='color: #1976d2;'>(초기화)</span>**
            3. **<span style='color: #1976d2; font-weight: bold;'>데이터 읽기</span>**: CSV에서 구조물 정보 가져오기 → `pd.read_csv()` **<span style='color: #1976d2;'>(초기화)</span>**
            4. **<span style='color: #388e3c; font-weight: bold;'>도형 그리기</span>**: 좌표에 맞춰 원과 사각형 배치 → `for row in data` **<span style='color: #388e3c;'>(반복문)</span>**
            
            **📊 결과**
            - 시각적 지도 완성 → `map.png`
            - 색깔별 구조물 구분 → `brown=건물, green=커피숍`
            - 격자와 라벨 표시 → `plt.grid(), plt.xlabel()`
            """, unsafe_allow_html=True)
    
    with st.expander("💻 핵심 시각화 코드 보기", expanded=False):
        st.markdown("**🔧 matplotlib 시각화 핵심 코드**")
        
        # 주석을 별도로 강조해서 표시
        st.markdown("**📝 핵심 로직 설명:**")
        st.markdown("""
        - **<span style='color: #1976d2; font-weight: bold;'>캔버스 생성</span>**: 그림을 그릴 도화지와 영역 설정 **<span style='color: #1976d2;'>(초기화)</span>**
        - **<span style='color: #1976d2; font-weight: bold;'>좌표계 설정</span>**: x, y 축 범위와 격자 표시 **<span style='color: #1976d2;'>(초기화)</span>**
        - **<span style='color: #388e3c; font-weight: bold;'>데이터 반복</span>**: CSV 데이터를 한 줄씩 읽어서 처리 **<span style='color: #388e3c;'>(반복문)</span>**
        - **<span style='color: #7b1fa2; font-weight: bold;'>도형 생성</span>**: 좌표에 맞춰 원과 사각형 그리기 **<span style='color: #7b1fa2;'>(도형 그리기)</span>**
        - **<span style='color: #f57c00; font-weight: bold;'>색깔 구분</span>**: 구조물 종류별로 다른 색깔 적용 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - **<span style='color: #f57c00; font-weight: bold;'>파일 저장</span>**: 완성된 지도를 PNG 파일로 저장 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        """, unsafe_allow_html=True)
        
        st.markdown("**💻 실제 코드 (주석 포함):**")
        
        # 주석을 굵은 색깔로 강조해서 표시
        st.markdown("**🎨 주석 색깔 의미:**")
        col_legend1, col_legend2, col_legend3 = st.columns(3)
        
        with col_legend1:
            st.markdown("""
            <span style="color:blue; font-weight:bold;">🔵 파란색</span> = 초기화 관련
            <span style="color:green; font-weight:bold;">🟢 초록색</span> = 반복문/루프
            """, unsafe_allow_html=True)
        
        with col_legend2:
            st.markdown("""
            <span style="color:red; font-weight:bold;">🔴 빨간색</span> = 조건 체크
            <span style="color:purple; font-weight:bold;">🟣 보라색</span> = 도형 그리기
            """, unsafe_allow_html=True)
        
        with col_legend3:
            st.markdown("""
            <span style="color:orange; font-weight:bold;">🟠 주황색</span> = 데이터 변환
            """, unsafe_allow_html=True)
        
        st.markdown("**🔍 라인별 주석 설명:**")
        col_comment1, col_comment2 = st.columns(2)
        
        with col_comment1:
            st.markdown("""
            **캔버스 설정:**
            - `plt.subplots(figsize=(8, 6))` <span style="color:blue; font-weight:bold;">← 그림 크기 설정</span>
            - `plt.xlim(0.5, 7.5)` <span style="color:blue; font-weight:bold;">← x축 범위 설정</span>
            - `plt.ylim(7.5, 15.5)` <span style="color:blue; font-weight:bold;">← y축 범위 설정</span>
            
            **데이터 처리:**
            - `for _, row in data.iterrows()` <span style="color:green; font-weight:bold;">← 데이터 한 줄씩 반복</span>
            - `x, y = int(row['x'])` <span style="color:orange; font-weight:bold;">← 좌표 추출</span>
            """, unsafe_allow_html=True)
        
        with col_comment2:
            st.markdown("""
            **도형 그리기:**
            - `Circle((x, y), 0.3)` <span style="color:purple; font-weight:bold;">← 원 그리기 (아파트/빌딩)</span>
            - `Rectangle((x-0.3, y-0.3), 0.6, 0.6)` <span style="color:purple; font-weight:bold;">← 사각형 그리기 (커피숍)</span>
            - `ax.add_patch(shape)` <span style="color:purple; font-weight:bold;">← 도형을 그림에 추가</span>
            
            **조건 체크:**
            - `if row['category'] in [1, 2]` <span style="color:red; font-weight:bold;">← 아파트/빌딩 체크</span>
            - `elif row['category'] == 4` <span style="color:red; font-weight:bold;">← 커피숍 체크</span>
            """, unsafe_allow_html=True)
        
        # 주석을 더 강조해서 보여주기
        st.info("🟡 **캔버스 생성** → `plt.subplots()`: 그림을 그릴 도화지와 영역을 만들기. figsize로 크기 조절                                    (초기화)")
        st.code("fig, ax = plt.subplots(figsize=(8, 6))  # (그림, 축) = 서브플롯생성(크기=(8, 6))", language='python')
        
        st.info("🟡 **좌표계 설정** → `plt.xlim()`: 지도의 x, y 축 범위를 정해서 보여질 영역 결정                                    (초기화)")
        st.code("plt.xlim(0.5, 7.5)  # x축범위 = 0.5부터 7.5까지\nplt.ylim(7.5, 15.5)  # y축범위 = 7.5부터 15.5까지", language='python')
        
        st.info("🟡 **데이터 반복** → `iterrows()`: 처리된 CSV 데이터를 한 줄씩 읽어서 각 구조물 정보 확인                                    (반복문)")
        st.code("for _, row in merged_data.iterrows():  # (인덱스무시, 행데이터)로 데이터반복", language='python')
        
        st.info("🟡 **좌표 추출** → `int(row['x'])`: CSV에서 읽은 문자열 좌표를 숫자로 변환해서 그리기 위치 결정                                    (데이터 변환)")
        st.code("x, y = int(row['x']), int(row['y'])  # (x좌표, y좌표) = 정수변환", language='python')
        
        st.info("🟡 **조건별 도형** → `if category in [1, 2]`: 구조물 종류에 따라 다른 모양과 색깔로 그리기                                    (조건 체크)")
        st.code("""if row['category'] in [1, 2]:  # 만약 카테고리가 [1, 2] 중 하나이면 (아파트, 빌딩)
    shape = Circle((x, y), 0.3, color='brown')  # 도형 = 원(중심=(x,y), 반지름=0.3, 색=갈색)""", language='python')
        
        st.info("🟡 **도형 추가** → `add_patch()`: 만든 도형(원, 사각형)을 실제 그림에 붙여넣기                                    (도형 그리기)")
        st.code("ax.add_patch(shape)  # 축.패치추가(도형) = 도형을 그림에 붙이기", language='python')
        
        st.info("🟡 **파일 저장** → `plt.savefig()`: 완성된 지도를 PNG 파일로 컴퓨터에 저장                                    (결과 저장)")
        st.code("plt.savefig('map.png', dpi=300, bbox_inches='tight')  # 그림저장(파일명, 해상도=300, 여백=최소)", language='python')
    
    with st.expander("📖 시각화 용어 설명", expanded=False):
        st.markdown("**💡 코드에서 사용된 주요 용어들**")
        
        col_term1, col_term2 = st.columns(2)
        
        with col_term1:
            st.markdown("""
            **📦 matplotlib 관련**
            - <span style='color: #1976d2; font-weight: bold;'>Figure</span>: 전체 그림 영역 (도화지) **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>Axes</span>: 실제 그래프가 그려지는 영역 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>subplot</span>: 하나의 Figure 안에 여러 그래프 영역 나누기 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>patch</span>: 원, 사각형 등의 도형 객체 **<span style='color: #7b1fa2;'>(도형 그리기)</span>**
            
            **🎨 도형 관련**
            - <span style='color: #7b1fa2; font-weight: bold;'>Circle</span>: 원을 그리는 클래스 (중심점, 반지름) **<span style='color: #7b1fa2;'>(도형 그리기)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>Rectangle</span>: 사각형을 그리는 클래스 (위치, 너비, 높이) **<span style='color: #7b1fa2;'>(도형 그리기)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>add_patch</span>: 도형을 그래프에 추가하는 함수 **<span style='color: #7b1fa2;'>(도형 그리기)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>color</span>: 도형의 색깔 지정 (brown, green 등) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            """, unsafe_allow_html=True)
        
        with col_term2:
            st.markdown("""
            **📍 좌표 관련**
            - <span style='color: #1976d2; font-weight: bold;'>xlim, ylim</span>: x축, y축의 표시 범위 설정 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>figsize</span>: 그림의 크기 (가로, 세로) 인치 단위 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>dpi</span>: 해상도 (Dots Per Inch) - 높을수록 선명 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>grid</span>: 격자 표시 여부 **<span style='color: #1976d2;'>(초기화)</span>**
            
            **⚙️ 파일 관련**
            - <span style='color: #f57c00; font-weight: bold;'>savefig</span>: 그림을 파일로 저장하는 함수 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>bbox_inches</span>: 여백 조정 ('tight'=최소 여백) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>PNG</span>: 이미지 파일 형식 (투명 배경 지원) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #388e3c; font-weight: bold;'>iterrows</span>: DataFrame을 행 단위로 반복하는 함수 **<span style='color: #388e3c;'>(반복문)</span>**
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **🎯 핵심 개념**
        - <span style='color: #f57c00; font-weight: bold;'>center</span>: 원의 중심점 좌표 (x, y) **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - <span style='color: #f57c00; font-weight: bold;'>radius</span>: 원의 반지름 크기 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - <span style='color: #f57c00; font-weight: bold;'>position</span>: 사각형의 왼쪽 아래 모서리 위치 **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - <span style='color: #1976d2; font-weight: bold;'>matplotlib.patches</span>: 도형 그리기 전용 모듈 **<span style='color: #1976d2;'>(초기화)</span>**
        """, unsafe_allow_html=True)
    
    if os.path.exists('map.png'):
        st.subheader("생성된 지도")
        
        # 이미지 표시
        image = Image.open('map.png')
        st.image(image, caption="반달곰 커피 지역 지도", use_container_width=True)
        
        # 범례 설명
        st.subheader("🔍 범례 설명")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **구조물 표현:**
            - 🟤 갈색 원: 아파트, 빌딩
            - 🟢 녹색 사각형: 반달곰커피
            - ⬜ 회색 사각형: 건설현장
            """)
        
        with col2:
            st.markdown("""
            **좌표계:**
            - X축: 가로 좌표 (1~7)
            - Y축: 세로 좌표 (1~8)
            - 격자: 각 셀은 1x1 크기
            """)
    else:
        st.warning("지도 파일(map.png)이 생성되지 않았습니다. 2단계를 먼저 실행해주세요.")
        
        if st.button("🗺 지도 생성하기"):
            with st.spinner("지도를 생성하는 중..."):
                import subprocess
                result = subprocess.run(['python', 'map_draw_real.py'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("지도가 성공적으로 생성되었습니다!")
                    st.rerun()
                else:
                    st.error(f"지도 생성 중 오류 발생: {result.stderr}")
    
    # 2단계 요점정리 박스 추가
    st.markdown("---")
    st.subheader("📝 2단계 요점정리")
    
    col_summary1, col_summary2 = st.columns(2)
    
    with col_summary1:
        st.success("""
**🎯 핵심 배운 내용**

✅ matplotlib로 그래프 그리기

✅ 좌표계 설정

✅ 도형 그리기

✅ 색깔 구분

✅ 파일 저장
        """)
    
    with col_summary2:
        st.info("""
**💡 실무에서 활용 가능한 기술**

🔹 보고서 그래프

🔹 대시보드

🔹 지도 시각화

🔹 프레젠테이션

🔹 웹사이트
        """)

elif stage == "3단계: 최단경로 탐색":
    st.header("🎯 3단계: 최단경로 탐색")
    
    # BFS 알고리즘 원리 설명
    st.subheader("🧠 BFS 알고리즘 원리")
    
    with st.expander("📚 최단경로 찾기 과정 이해하기", expanded=False):
        col_explain1, col_explain2 = st.columns(2)
        
        with col_explain1:
            st.markdown("""
            **🔍 BFS (Breadth-First Search) 란?**
            - **너비 우선 탐색**: 가까운 곳부터 차례대로 탐색 → `queue`
            - **최단경로 보장**: 가장 적은 이동으로 목적지 도달 → `path`
            - **4방향 이동**: 상하좌우로만 이동 가능 → `directions`
            
            **🚧 장애물 설정**
            - 아파트/빌딩: 지나갈 수 없음 → `obstacle`
            - 건설현장: 지나갈 수 없음 → `obstacle`
            - 빈 공간: 자유롭게 이동 가능 → `free`
            """)
        
        with col_explain2:
            st.markdown("""
            **⚙️ 탐색 과정**
            1. **<span style='color: #1976d2; font-weight: bold;'>시작점</span>**에서 출발 → `start` **<span style='color: #1976d2;'>(초기화)</span>**
            2. **<span style='color: #f57c00; font-weight: bold;'>인접한 4방향</span>** 확인 → `dx, dy` **<span style='color: #f57c00;'>(데이터 변환)</span>**
            3. **<span style='color: #7b1fa2; font-weight: bold;'>갈 수 있는 곳</span>**을 큐에 추가 → `append` **<span style='color: #7b1fa2;'>(경로 확장)</span>**
            4. **<span style='color: #1976d2; font-weight: bold;'>방문 표시</span>**로 중복 방지 → `visited` **<span style='color: #1976d2;'>(초기화)</span>**
            5. **<span style='color: #388e3c; font-weight: bold;'>목적지 발견</span>**까지 반복 → `while` **<span style='color: #388e3c;'>(반복문)</span>**
            
            **📊 결과**
            - 최단 이동 거리 계산 → `len(path)`
            - 경로상의 모든 좌표 저장 → `[(x,y), ...]`
            - 시각화로 경로 표시 → `plt.plot`
            """, unsafe_allow_html=True)
    
    with st.expander("💻 핵심 알고리즘 코드 보기", expanded=False):
        st.markdown("**🔧 BFS 최단경로 탐색 핵심 코드**")
        
        # 주석을 별도로 강조해서 표시
        st.markdown("**📝 핵심 로직 설명:**")
        st.markdown("""
        - **<span style='color: #1976d2; font-weight: bold;'>BFS 초기화</span>**: 큐에 시작점 저장, 방문 기록 시작 **<span style='color: #1976d2;'>(초기화)</span>**
        - **<span style='color: #1976d2; font-weight: bold;'>4방향 이동</span>**: 상하좌우 좌표 변화량 설정 **<span style='color: #1976d2;'>(초기화)</span>**
        - **<span style='color: #388e3c; font-weight: bold;'>큐에서 꺼내기</span>**: 현재 위치와 지금까지의 경로 가져오기 **<span style='color: #388e3c;'>(반복문)</span>**
        - **<span style='color: #d32f2f; font-weight: bold;'>목적지 확인</span>**: 현재 위치가 목표와 같은지 체크 **<span style='color: #d32f2f;'>(조건 체크)</span>**
        - **<span style='color: #d32f2f; font-weight: bold;'>방문/범위 체크</span>**: 이미 간 곳이거나 범위 밖이면 패스 **<span style='color: #d32f2f;'>(조건 체크)</span>**
        - **<span style='color: #d32f2f; font-weight: bold;'>장애물 체크</span>**: 건물이나 건설현장이면 패스 **<span style='color: #d32f2f;'>(조건 체크)</span>**
        - **<span style='color: #7b1fa2; font-weight: bold;'>경로 확장</span>**: 갈 수 있는 곳이면 경로에 추가해서 큐에 넣기 **<span style='color: #7b1fa2;'>(경로 확장)</span>**
        """, unsafe_allow_html=True)
        
        st.markdown("**💻 실제 코드 (주석 포함):**")
        
        # 주석을 굵은 색깔로 강조해서 표시
        st.markdown("**🎨 주석 색깔 의미:**")
        col_legend1, col_legend2, col_legend3 = st.columns(3)
        
        with col_legend1:
            st.markdown("""
            <span style="color:blue; font-weight:bold;">🔵 파란색</span> = 초기화 관련
            <span style="color:green; font-weight:bold;">🟢 초록색</span> = 반복문/루프
            """, unsafe_allow_html=True)
        
        with col_legend2:
            st.markdown("""
            <span style="color:red; font-weight:bold;">🔴 빨간색</span> = 조건 체크
            <span style="color:purple; font-weight:bold;">🟣 보라색</span> = 경로 확장
            """, unsafe_allow_html=True)
        
        with col_legend3:
            st.markdown("""
            <span style="color:orange; font-weight:bold;">🟠 주황색</span> = 데이터 변환
            """, unsafe_allow_html=True)
        
        st.markdown("**🔍 라인별 주석 설명:**")
        col_comment1, col_comment2 = st.columns(2)
        
        with col_comment1:
            st.markdown("""
            **초기화 부분:**
            - `queue = deque([...])` <span style="color:blue; font-weight:bold;">← 큐에 시작점과 경로 저장</span>
            - `visited = {start}` <span style="color:blue; font-weight:bold;">← 방문한 곳 기록용 집합</span>
            - `directions = [...]` <span style="color:blue; font-weight:bold;">← 상하좌우 이동 방향</span>
            
            **메인 탐색 루프:**
            - `while queue:` <span style="color:green; font-weight:bold;">← 큐가 빌 때까지 반복</span>
            - `queue.popleft()` <span style="color:green; font-weight:bold;">← 큐에서 맨 앞 데이터 꺼내기</span>
            """, unsafe_allow_html=True)
        
        with col_comment2:
            st.markdown("""
            **조건 체크:**
            - `if (current_x, current_y) == end:` <span style="color:red; font-weight:bold;">← 목적지 도달 확인</span>
            - `if next_pos in visited:` <span style="color:red; font-weight:bold;">← 이미 방문한 곳인지 체크</span>
            - `if grid_map[next_pos] == 'obstacle':` <span style="color:red; font-weight:bold;">← 장애물인지 체크</span>
            
            **경로 확장:**
            - `visited.add(next_pos)` <span style="color:purple; font-weight:bold;">← 방문 처리</span>
            - `new_path = path + [next_pos]` <span style="color:purple; font-weight:bold;">← 경로에 새 위치 추가</span>
            """, unsafe_allow_html=True)
        
        # 주석을 더 강조해서 보여주기
        st.info("🟡 **BFS 초기화** → `queue = deque()`: 탐색할 곳들을 순서대로 저장하는 줄. 시작점과 경로를 함께 넣어둠                                    (초기화)")
        st.code("queue = deque([(start, [start])])", language='python')
        
        st.info("🟡 **방문 기록** → `visited = {start}`: 이미 간 곳들을 기록해서 중복 방지. set은 중복 안 들어감                                    (초기화)")
        st.code("visited = {start}", language='python')
        
        st.info("🟡 **이동 방향** → `directions = [(0,1), ...]`: 상하좌우 4방향 좌표 변화량. 나중에 현재위치에 더해서 새 위치 계산                                    (초기화)")
        st.code("directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]", language='python')
        
        st.info("🟡 **탐색 시작** → `while queue:`: 큐에 뭔가 있는 동안 계속 반복. 큐가 비면 더 갈 곳 없음                                    (반복문)")
        st.code("while queue:", language='python')
        
        st.info("🟡 **현재 위치 꺼내기** → `popleft()`: 큐에서 맨 앞 것을 꺼냄. BFS는 가까운 곳부터 확인하는 방식                                    (반복문)")
        st.code("(current_x, current_y), path = queue.popleft()  # (현재x, 현재y), 지금까지경로", language='python')
        
        st.info("🟡 **목적지 확인** → `if (x,y) == end:`: 현재 위치가 커피숍인지 확인. 맞으면 경로 반환하고 끝                                    (조건 체크)")
        st.code("""if (current_x, current_y) == end:
    return path""", language='python')
        
        st.info("🟡 **4방향 탐색** → `for dx, dy in directions:`: 상하좌우 각 방향으로 한칸씩 이동한 새 좌표 계산                                    (반복문)")
        st.code("""for dx, dy in directions:  # (델타x, 델타y) = 좌표 변화량
    next_x = current_x + dx  # 다음 x좌표 = 현재 x + 변화량
    next_y = current_y + dy  # 다음 y좌표 = 현재 y + 변화량  
    next_pos = (next_x, next_y)  # 다음 위치 = (x, y) 튜플""", language='python')
        
        st.info("🟡 **중복/범위 체크** → `if in visited or not in grid_map:`: 이미 간 곳이거나 지도 밖이면 건너뛰기                                    (조건 체크)")
        st.code("""if next_pos in visited or next_pos not in grid_map:
    continue""", language='python')
        
        st.info("🟡 **장애물 체크** → `if == 'obstacle':`: 아파트나 빌딩 같은 장애물이면 지나갈 수 없으니 건너뛰기                                    (조건 체크)")
        st.code("""if grid_map[next_pos] == 'obstacle':
    continue""", language='python')
        
        st.info("🟡 **갈 수 있는 곳 처리** → `visited.add()` + `path +` + `queue.append()`: 방문표시 → 경로확장 → 큐에추가                                    (경로 확장)")
        st.code("""visited.add(next_pos)  # 방문기록에 추가 (중복방지)
new_path = path + [next_pos]  # 기존경로 + 새위치 = 확장된경로
queue.append((next_pos, new_path))  # 큐에 (새위치, 새경로) 추가""", language='python')
        
        st.info("🟡 **경로 없음** → `return []`: 큐가 다 비었는데 목적지 못 찾았으면 갈 수 없다는 뜻                                    (반환)")
        st.code("return []", language='python')
        
        st.markdown("**🏗️ 장애물 설정 코드**")
        
        st.markdown("**📝 장애물 설정 로직:**")
        st.markdown("""
        - **CSV 데이터 읽기**: 각 좌표의 건설현장과 건물 정보 확인
        - **건설현장 체크**: ConstructionSite가 1이면 장애물로 설정
        - **건물 체크**: category가 1(아파트)이나 2(빌딩)면 장애물로 설정
        - **빈 공간**: 위 조건에 해당 안 하면 자유롭게 이동 가능한 곳으로 설정
        """)
        
        st.markdown("**💻 실제 코드 (주석 포함):**")
        
        st.markdown("**🎨 주석 색깔 의미:**")
        st.markdown("""
        <span style="color:blue; font-weight:bold;">🔵 파란색</span> = 초기화 관련 | 
        <span style="color:green; font-weight:bold;">🟢 초록색</span> = 반복문/루프 | 
        <span style="color:orange; font-weight:bold;">🟠 주황색</span> = 데이터 변환 | 
        <span style="color:red; font-weight:bold;">🔴 빨간색</span> = 조건 체크 | 
        <span style="color:purple; font-weight:bold;">🟣 보라색</span> = 기타
        """, unsafe_allow_html=True)
        
        st.markdown("**🔍 라인별 주석 설명:**")
        st.markdown("""
        - `grid_map = {}` <span style="color:blue; font-weight:bold;">← 좌표별 상태를 저장할 딕셔너리 생성</span>
        - `for _, row in data.iterrows():` <span style="color:green; font-weight:bold;">← CSV 데이터를 한 줄씩 읽기</span>
        - `x, y = int(row['x']), int(row['y'])` <span style="color:orange; font-weight:bold;">← 좌표값을 정수로 변환</span>
        - `row['ConstructionSite'] == 1` <span style="color:red; font-weight:bold;">← 건설현장 여부 체크</span>
        - `row['category'] in [1, 2]` <span style="color:purple; font-weight:bold;">← 아파트(1) 또는 빌딩(2) 체크</span>
        """, unsafe_allow_html=True)
        
        st.info("🟡 **지도 초기화** → `grid_map = {}`: 각 좌표별로 갈 수 있는지 없는지 저장할 딕셔너리                                    (초기화)")
        st.code("grid_map = {}", language='python')
        
        st.info("🟡 **CSV 읽기** → `for _, row in data.iterrows()`: 판다스로 CSV 파일 한 줄씩 읽어오기                                    (반복문)")
        st.code("for _, row in data.iterrows():", language='python')
        
        st.info("🟡 **좌표 변환** → `x, y = int(row['x'])`: CSV의 문자열을 숫자로 바꿔서 x, y 좌표 만들기                                    (데이터 변환)")
        st.code("x, y = int(row['x']), int(row['y'])  # (x좌표, y좌표) = 정수변환", language='python')
        
        st.info("🟡 **건설현장 체크** → `if row['ConstructionSite'] == 1:`: 건설 중이면 1이니까 장애물로 설정                                    (조건 체크)")
        st.code("""if row['ConstructionSite'] == 1:  # 건설현장이면
    grid_map[(x, y)] = 'obstacle'  # 장애물로 설정""", language='python')
        
        st.info("🟡 **건물 체크** → `elif row['category'] in [1, 2]:`: 아파트(1)나 빌딩(2)도 장애물로 설정                                    (조건 체크)")
        st.code("""elif row['category'] in [1, 2]:  # 아파트(1) 또는 빌딩(2)이면
    grid_map[(x, y)] = 'obstacle'  # 장애물로 설정""", language='python')
        
        st.info("🟡 **빈 공간** → `else: grid_map = 'free'`: 나머지는 다 갈 수 있는 빈 공간으로 설정                                    (기타)")
        st.code("""else:  # 그 외에는 (빈공간, 커피숍, 집 등)
    grid_map[(x, y)] = 'free'  # 자유롭게 이동가능""", language='python')
        
        st.info("🟡 **지도 완성** → `return grid_map`: 모든 좌표 정보가 담긴 완성된 지도 반환                                    (반환)")
        st.code("return grid_map", language='python')
    
    with st.expander("🎮 실제 탐색 과정 시뮬레이션", expanded=False):
        st.markdown("**🚀 MyHome(7,2)에서 BandalgomCoffee(2,5)까지 실제 탐색 과정**")
        
        # 1단계: 초기화
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **1단계: BFS 시작 준비**
            - 시작점 (7,2)에서 출발
            - 큐에 시작 위치와 경로 저장
            - 방문 기록 초기화
            - 목표점 (2,5) 설정
            """)
        with col2:
            st.code('''
queue = deque([((7,2), [(7,2)])])
visited = {(7,2)}
start = (7,2)
end = (2,5)

print(f"시작: {start}, 목표: {end}")
            ''', language='python')
        
        # 2단계: 4방향 탐색
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **2단계: 첫 위치에서 4방향 확인**
            - 큐에서 현재 위치 꺼내기
            - 상하좌우 4방향 좌표 계산
            - 각 방향의 이동 가능성 확인
            - (7,2) 주변은 모두 장애물
            """)
        with col2:
            st.code('''
(current_x, current_y), path = queue.popleft()
directions = [(0,1), (0,-1), (-1,0), (1,0)]

for dx, dy in directions:
    next_x = current_x + dx
    next_y = current_y + dy
    next_pos = (next_x, next_y)
    print(f"확인: {next_pos}")
            ''', language='python')
        
        # 3단계: 장애물 확인
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **3단계: 이동 가능성 판단**
            - 이미 방문한 곳인지 확인
            - 지도 범위를 벗어났는지 확인
            - 장애물(건설현장, 건물)인지 확인
            - 조건을 통과하면 큐에 추가
            """)
        with col2:
            st.code('''
if next_pos in visited:
    continue  # 이미 방문함
    
if next_pos not in grid_map:
    continue  # 범위 초과
    
if grid_map[next_pos] == 'obstacle':
    continue  # 장애물
    
# 이동 가능한 경우
visited.add(next_pos)
queue.append((next_pos, new_path))
            ''', language='python')
        
        # 4단계: 우회 경로
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **4단계: 우회 경로 탐색**
            - BFS는 자동으로 다른 경로 시도
            - 여러 단계를 거쳐 (6,6) 등에 도달
            - 이동 가능한 모든 방향을 큐에 추가
            - 체계적으로 모든 경로 탐색
            """)
        with col2:
            st.code('''
# 몇 단계 후 (6,6)에서:
current_pos = (6,6)

for dx, dy in directions:
    next_pos = (6+dx, 6+dy)
    
    if grid_map[next_pos] == 'free':
        visited.add(next_pos)
        new_path = path + [next_pos]
        queue.append((next_pos, new_path))
            ''', language='python')
        
        # 5단계: 목표 발견
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **5단계: 목표 발견 및 완료**
            - (3,5)에서 좌측 확인 시 (2,5) 발견
            - 목표점과 일치하는지 확인
            - 최종 경로 완성 및 반환
            - 총 25단계의 최단 경로 완성
            """)
        with col2:
            st.code('''
# (3,5)에서 목표 발견:
if next_pos == end:
    final_path = path + [next_pos]
    print("목표 발견!")
    print(f"최단경로: {len(final_path)}단계")
    return final_path

# 결과: [(7,2), ..., (2,5)]
            ''', language='python')
    
    with st.expander("📖 프로그래밍 용어 설명", expanded=False):
        st.markdown("**💡 코드에서 사용된 주요 용어들**")
        
        col_term1, col_term2 = st.columns(2)
        
        with col_term1:
            st.markdown("""
            **📦 데이터 구조**
            - <span style='color: #1976d2; font-weight: bold;'>queue (큐)</span>: 먼저 들어간 것이 먼저 나오는 구조 (FIFO) **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>deque</span>: 양쪽 끝에서 추가/제거가 가능한 큐 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>set</span>: 중복이 없는 데이터 집합 (방문 기록용) **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>tuple</span>: 변경할 수 없는 순서쌍 (x, y 좌표 등) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            
            **🔄 반복문 관련**
            - <span style='color: #388e3c; font-weight: bold;'>for</span>: 정해진 범위나 목록을 반복 **<span style='color: #388e3c;'>(반복문)</span>**
            - <span style='color: #388e3c; font-weight: bold;'>while</span>: 조건이 참인 동안 반복 **<span style='color: #388e3c;'>(반복문)</span>**
            - <span style='color: #d32f2f; font-weight: bold;'>continue</span>: 현재 반복을 건너뛰고 다음으로 **<span style='color: #d32f2f;'>(조건 체크)</span>**
            - <span style='color: #388e3c; font-weight: bold;'>break</span>: 반복문을 완전히 종료 **<span style='color: #388e3c;'>(반복문)</span>**
            """, unsafe_allow_html=True)
        
        with col_term2:
            st.markdown("""
            **📍 좌표 관련**
            - <span style='color: #f57c00; font-weight: bold;'>dx, dy</span>: 델타 X, 델타 Y (좌표 변화량) **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>current_x, current_y</span>: 현재 X, Y 좌표 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #f57c00; font-weight: bold;'>next_x, next_y</span>: 다음 이동할 X, Y 좌표 **<span style='color: #f57c00;'>(데이터 변환)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>directions</span>: 이동 방향들 (상하좌우) **<span style='color: #1976d2;'>(초기화)</span>**
            
            **⚙️ 알고리즘 관련**
            - <span style='color: #7b1fa2; font-weight: bold;'>BFS</span>: Breadth-First Search (너비 우선 탐색) **<span style='color: #7b1fa2;'>(기타)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>visited</span>: 이미 방문한 곳들의 기록 **<span style='color: #1976d2;'>(초기화)</span>**
            - <span style='color: #7b1fa2; font-weight: bold;'>path</span>: 지금까지 이동한 경로 **<span style='color: #7b1fa2;'>(경로 확장)</span>**
            - <span style='color: #1976d2; font-weight: bold;'>grid_map</span>: 격자 형태의 지도 데이터 **<span style='color: #1976d2;'>(초기화)</span>**
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **🎯 핵심 개념**
        - <span style='color: #388e3c; font-weight: bold;'>popleft()</span>: 큐의 맨 앞에서 데이터 꺼내기 **<span style='color: #388e3c;'>(반복문)</span>**
        - <span style='color: #7b1fa2; font-weight: bold;'>append()</span>: 리스트나 큐의 끝에 데이터 추가 **<span style='color: #7b1fa2;'>(경로 확장)</span>**
        - <span style='color: #f57c00; font-weight: bold;'>obstacle</span>: 장애물 (지나갈 수 없는 곳) - **이 프로젝트 전용 데이터값** **<span style='color: #f57c00;'>(데이터 변환)</span>**
        - <span style='color: #1976d2; font-weight: bold;'>range</span>: 숫자 범위 생성 (예: range(1, 8) → 1,2,3,4,5,6,7) **<span style='color: #1976d2;'>(초기화)</span>**
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if os.path.exists('map_final.png'):
            st.subheader("최단경로가 표시된 지도")
            image = Image.open('map_final.png')
            st.image(image, caption="최단경로 시각화", use_container_width=True)
        else:
            st.warning("최단경로 지도(map_final.png)가 생성되지 않았습니다.")
            
            if st.button("🎯 최단경로 찾기"):
                with st.spinner("최단경로를 계산하는 중..."):
                    import subprocess
                    result = subprocess.run(['python', 'map_direct_save.py'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.success("최단경로가 성공적으로 계산되었습니다!")
                        st.rerun()
                    else:
                        st.error(f"경로 계산 중 오류 발생: {result.stderr}")
    
    with col2:
        # 경로 데이터 표시
        if os.path.exists('home_to_cafe.csv'):
            st.subheader("📊 경로 데이터")
            path_data = pd.read_csv('home_to_cafe.csv')
            st.dataframe(path_data)
            
            st.subheader("📈 경로 정보")
            st.metric("총 이동 거리", f"{len(path_data) - 1}칸")
            st.metric("총 단계 수", f"{len(path_data)}단계")
            
            # 시작점과 끝점 표시
            if len(path_data) > 0:
                start = (path_data.iloc[0]['x'], path_data.iloc[0]['y'])
                end = (path_data.iloc[-1]['x'], path_data.iloc[-1]['y'])
                st.write(f"**시작점**: {start}")
                st.write(f"**도착점**: {end}")
        else:
            st.info("경로 데이터(home_to_cafe.csv)가 아직 생성되지 않았습니다.")
    
    # 3단계 요점정리 박스 추가
    st.markdown("---")
    st.subheader("📝 3단계 요점정리")
    
    col_summary1, col_summary2 = st.columns(2)
    
    with col_summary1:
        st.success("""
**🎯 핵심 배운 내용**

✅ BFS 알고리즘

✅ 큐(Queue) 사용

✅ 방문 기록

✅ 4방향 탐색

✅ 조건 분기
        """)
    
    with col_summary2:
        st.info("""
**💡 실무에서 활용 가능한 기술**

🔹 네비게이션

🔹 게임 개발

🔹 물류 최적화

🔹 네트워크 분석

🔹 로봇 공학
        """)
    
    st.warning("""
**🎓 이 프로젝트로 배운 전체 기술 스택**

**1단계 pandas** → **2단계 matplotlib** → **3단계 BFS 알고리즘**

이제 여러분은 **데이터 수집, 시각화, 최적화 알고리즘**을 모두 다룰 수 있는 개발자가 되었습니다! 
실제 IT 기업에서 사용하는 핵심 기술들을 모두 경험해보셨습니다.
    """)

# 푸터
st.markdown("---")
st.markdown("**반달곰 커피 프로젝트** | 코디세이 AI 올인원 프로그램 (업데이트됨)")