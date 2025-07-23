"""
1단계: 데이터 수집 및 분석
반달곰 커피 프로젝트의 첫 번째 단계로 CSV 파일들을 불러와 분석합니다.
"""

import pandas as pd


def load_and_analyze_data():
    """
    CSV 파일들을 불러와 분석하고 병합하는 함수
    
    Returns:
        pandas.DataFrame: 병합된 데이터프레임
    """
    # CSV 파일들 불러오기
    print('=== 데이터 파일 불러오기 ===')
    
    area_map = pd.read_csv('area_map.csv')
    print('area_map.csv 내용:')
    print(area_map.head())
    print(f'데이터 크기: {area_map.shape}\n')
    
    area_struct = pd.read_csv('area_struct.csv')
    print('area_struct.csv 내용:')
    print(area_struct.head())
    print(f'데이터 크기: {area_struct.shape}\n')
    
    area_category = pd.read_csv('area_category.csv')
    print('area_category.csv 내용:')
    print(area_category.head())
    print(f'데이터 크기: {area_category.shape}\n')
    
    # 구조물 카테고리를 이름으로 변환 (category 0은 빈 공간)
    print('=== 구조물 카테고리를 이름으로 변환 ===')
    area_struct_named = area_struct.merge(
        area_category, 
        on='category', 
        how='left'
    )
    print('구조물 카테고리가 이름으로 변환된 데이터:')
    print(area_struct_named[area_struct_named['category'] != 0].head(10))
    print()
    
    # 세 데이터를 하나의 DataFrame으로 병합
    print('=== 데이터 병합 ===')
    merged_data = area_map.merge(
        area_struct_named, 
        on=['x', 'y'], 
        how='left'
    )
    
    # 좌표 기준으로 정렬
    merged_data = merged_data.sort_values(['x', 'y']).reset_index(drop=True)
    print('병합된 전체 데이터:')
    print(merged_data.head(10))
    print(f'전체 데이터 크기: {merged_data.shape}\n')
    
    # area 1에 대한 데이터만 필터링 (반달곰 커피가 있는 지역)
    print('=== area 1 데이터 필터링 ===')
    area_1_data = merged_data[merged_data['area'] == 1].copy()
    print('area 1 필터링된 데이터:')
    print(area_1_data.head(10))
    print(f'area 1 데이터 크기: {area_1_data.shape}\n')
    
    return area_1_data


def generate_structure_report(data):
    """
    구조물 종류별 요약 통계를 생성하는 함수 (보너스)
    
    Args:
        data (pandas.DataFrame): 분석할 데이터프레임
    """
    print('=== 구조물 종류별 요약 통계 (보너스) ===')
    
    # 구조물이 있는 데이터만 추출 (category가 0이 아닌 것들)
    structures = data[data['category'] != 0].copy()
    
    if not structures.empty:
        # struct 열이 NaN이 아닌 것들만
        structures_with_names = structures.dropna(subset=['struct'])
        
        if not structures_with_names.empty:
            structure_summary = structures_with_names.groupby('struct').agg({
                'x': 'count',
                'area': 'first'
            }).rename(columns={'x': '개수', 'area': '지역'})
            
            print('구조물 종류별 통계:')
            print(structure_summary)
            print()
            
            # 각 구조물의 위치 정보
            print('구조물별 상세 위치:')
            for struct_name in structures_with_names['struct'].unique():
                struct_locations = structures_with_names[structures_with_names['struct'] == struct_name][['x', 'y']]
                print(f'{struct_name}: {list(zip(struct_locations["x"], struct_locations["y"]))}')
        else:
            print('구조물 이름 데이터가 없습니다.')
    else:
        print('구조물 데이터가 없습니다.')
    
    print()


def main():
    """
    메인 실행 함수
    """
    print('반달곰 커피 데이터 분석 프로젝트 - 1단계')
    print('=' * 50)
    
    # 데이터 불러오기 및 분석
    filtered_data = load_and_analyze_data()
    
    # 보너스: 구조물 종류별 요약 통계 생성
    generate_structure_report(filtered_data)
    
    print('1단계 데이터 분석 완료!')
    
    return filtered_data


if __name__ == '__main__':
    result_data = main()