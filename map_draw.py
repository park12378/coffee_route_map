"""
2단계: 지도 시각화
반달곰 커피 프로젝트의 두 번째 단계로 분석된 데이터를 기반으로 지역 지도를 시각화합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def load_processed_data():
    """
    1단계에서 처리된 데이터를 다시 불러오는 함수
    
    Returns:
        pandas.DataFrame: 처리된 데이터프레임
    """
    # CSV 파일들 불러오기
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_category = pd.read_csv('area_category.csv')
    
    # 구조물 ID를 이름으로 변환
    area_struct_named = area_struct.merge(
        area_category, 
        on='struct_id', 
        how='left'
    )
    
    # 세 데이터를 하나의 DataFrame으로 병합
    merged_data = area_map.merge(
        area_struct_named, 
        on=['area', 'x', 'y'], 
        how='left'
    )
    
    # area 1에 대한 데이터만 필터링
    area_1_data = merged_data[merged_data['area'] == 1].copy()
    
    return area_1_data


def create_map_visualization(data):
    """
    지도 시각화를 생성하는 함수
    
    Args:
        data (pandas.DataFrame): 시각화할 데이터프레임
    """
    # 좌표 범위 확인
    x_min, x_max = data['x'].min(), data['x'].max()
    y_min, y_max = data['y'].min(), data['y'].max()
    
    print(f'좌표 범위: x({x_min}-{x_max}), y({y_min}-{y_max})')
    
    # 그래프 설정
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 좌표계 설정 (좌측 상단이 (1,1), 우측 하단이 최대값)
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_max + 0.5, y_min - 0.5)  # y축 뒤집기
    
    # 격자 라인 그리기
    for x in range(x_min, x_max + 1):
        ax.axvline(x, color='lightgray', linestyle='-', alpha=0.5)
    for y in range(y_min, y_max + 1):
        ax.axhline(y, color='lightgray', linestyle='-', alpha=0.5)
    
    # 구조물별 시각화
    structure_colors = {
        '아파트': 'brown',
        '빌딩': 'brown',
        '반달곰커피': 'green',
        '내집': 'green',
        '건설현장': 'gray'
    }
    
    structure_markers = {
        '아파트': 'o',      # 원형
        '빌딩': 'o',        # 원형
        '반달곰커피': 's',   # 사각형
        '내집': '^',        # 삼각형
        '건설현장': 's'      # 사각형
    }
    
    structure_sizes = {
        '아파트': 200,
        '빌딩': 200,
        '반달곰커피': 300,
        '내집': 250,
        '건설현장': 400
    }
    
    # 범례를 위한 핸들 저장
    legend_handles = []
    legend_labels = []
    
    # 구조물이 있는 좌표 시각화
    structures = data.dropna(subset=['struct_name'])
    
    for struct_name in structures['struct_name'].unique():
        struct_data = structures[structures['struct_name'] == struct_name]
        
        scatter = ax.scatter(
            struct_data['x'], 
            struct_data['y'],
            c=structure_colors[struct_name],
            marker=structure_markers[struct_name],
            s=structure_sizes[struct_name],
            alpha=0.8,
            edgecolors='black',
            linewidth=1
        )
        
        # 범례용 핸들 저장
        legend_handles.append(scatter)
        legend_labels.append(struct_name)
        
        print(f'{struct_name} 위치: {list(zip(struct_data["x"], struct_data["y"]))}')
    
    # 축 설정
    ax.set_xlabel('X 좌표', fontsize=12)
    ax.set_ylabel('Y 좌표', fontsize=12)
    ax.set_title('반달곰 커피 지역 지도', fontsize=16, fontweight='bold')
    
    # 격자 눈금 설정
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    
    # 범례 추가 (보너스)
    if legend_handles:
        ax.legend(
            legend_handles, 
            legend_labels, 
            loc='upper left', 
            bbox_to_anchor=(1.02, 1),
            fontsize=10
        )
    
    # 그래프 조정
    plt.tight_layout()
    
    # 이미지 저장
    plt.savefig('map.png', dpi=300, bbox_inches='tight')
    print('지도가 map.png 파일로 저장되었습니다.')
    
    # 화면에 표시
    plt.show()
    
    return fig, ax


def main():
    """
    메인 실행 함수
    """
    print('반달곰 커피 지도 시각화 프로젝트 - 2단계')
    print('=' * 50)
    
    # 데이터 불러오기
    data = load_processed_data()
    print(f'불러온 데이터 크기: {data.shape}')
    print()
    
    # 지도 시각화 생성
    create_map_visualization(data)
    
    print('2단계 지도 시각화 완료!')


if __name__ == '__main__':
    main()
