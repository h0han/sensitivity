import os
import pandas as pd

# 'Result' 디렉토리 내의 모든 .csv 파일을 찾아 리스트에 저장
directory = 'Result'
csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]

# 결과를 저장할 빈 DataFrame 생성
result_df = pd.DataFrame()

# 각 .csv 파일에 대하여
for csv_file in csv_files:
    # 파일을 읽고
    df = pd.read_csv(csv_file)

    # 두 번째 열을 가져와서 결과 DataFrame에 추가
    result_df = pd.concat([result_df, df.iloc[:, 1]], axis=1)

# 결과를 저장
result_df.to_csv('concatenated.csv', index=False)
print("done")