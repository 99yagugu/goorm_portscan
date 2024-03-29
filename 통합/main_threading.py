import concurrent.futures
import time
from scan import *

def scan_all(host):
    # 각 스캔 작업을 함수와 연관 메타데이터(포트 번호)와 함께 정의
    scan_tasks = [
    (Telnet_scan, {}),
    (SMTP_scan, {}),
    (DNS_scan, {})
]

    results = []  # 결과를 저장할 리스트

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 각 스캔 작업에 대한 future 생성
        futures = [executor.submit(task[0], host, **task[1]) for task in scan_tasks]

        # 모든 future 완료를 기다리고 결과 저장
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                # 예외 발생 시 오류 메시지에 올바른 포트 번호를 포함
                task_index = futures.index(future)
                task_metadata = scan_tasks[task_index][1]
                error_result = {'port': task_metadata['port'], 'status': 'error', 'error_message': str(e)}
                results.append(error_result)

    # 결과를 포트 번호에 따라 정렬
    sorted_results = sorted(results, key=lambda x: x['port'] if isinstance(x, dict) else x[0]['port'])

    # 정렬된 결과 출력   
    for result in sorted_results:
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        print()
    

if __name__ == "__main__":

    host =  '192.168.0.48'
    
    startTime = time.time()
    
    scan_all(host)
    
    endTime = time.time()
    
    print("Executed Time:", (endTime - startTime))
