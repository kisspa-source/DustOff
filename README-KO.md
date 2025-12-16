# DustOff - 윈도우 앱 관리 및 메모리 최적화 프로그램

![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

깔끔하고 트렌디한 UI를 갖춘 Windows 11용 애플리케이션 관리 및 메모리 최적화 프로그램입니다.

## 주요 기능

### 📊 메모리 대시보드
- 실시간 메모리 사용량 모니터링
- 색상 인디케이터가 있는 시각적 진행률 바 (파랑/빨강)
- 원클릭 메모리 최적화
- 상위 10개 메모리 사용 프로세스 목록

### 📦 애플리케이션 관리
- 설치된 모든 애플리케이션 스캔 및 목록 표시
- 실행 파일에서 추출한 앱 아이콘 표시
- 버전, 용량, 설치 날짜 표시
- 실행 중인 애플리케이션 감지 (프로세스 수 표시)
- 모든 컬럼 정렬 지원
- 빠른 삭제 옵션

### ⚡ 메모리 최적화
- 모든 프로세스의 워킹셋 정리
- 즉각적인 RAM 회수
- 최적화 결과 시각적 피드백

## 스크린샷

*메모리 대시보드와 앱 목록이 있는 애플리케이션 인터페이스*

## 설치 방법

### 소스에서 실행
```bash
# 저장소 클론
git clone https://github.com/yourusername/DustOff.git
cd DustOff

# 의존성 설치
pip install PySide6 psutil wmi pywin32

# 애플리케이션 실행
python main.py
```

### 독립 실행 파일
`dist/DustOff` 폴더에서 최신 릴리스를 다운로드하고 `DustOff.exe`를 실행하세요.

## 실행 파일 빌드

```bash
pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --name DustOff --add-data "ui;ui" --add-data "core;core" main.py
```

실행 파일은 `dist/DustOff/DustOff.exe`에 생성됩니다.

## 프로젝트 구조

```
DustOff/
├── main.py                 # 애플리케이션 진입점
├── core/
│   ├── app_scanner.py      # Windows 레지스트리 앱 스캐너
│   ├── icon_extractor.py   # Windows 아이콘 추출
│   ├── memory_opt.py       # 메모리 최적화 로직
│   ├── process_matcher.py  # 실행 중인 프로세스 매칭
│   └── system_info.py      # 시스템 정보 조회
├── ui/
│   ├── app_list.py         # 애플리케이션 목록 위젯
│   ├── dashboard.py        # 메모리 대시보드 위젯
│   ├── main_window.py      # 메인 윈도우 컨테이너
│   └── styles.py           # UI 스타일 및 테마
└── dist/
    └── DustOff/
        └── DustOff.exe     # 독립 실행 파일
```

## 요구 사항

- Windows 10/11
- Python 3.10+ (소스 실행 시)
- 의존성:
  - PySide6
  - psutil
  - pywin32
  - wmi

## 기술 스택

- **GUI 프레임워크**: PySide6 (Qt for Python)
- **시스템 API**: psutil, win32gui, winreg
- **패키징**: PyInstaller

## 라이선스

MIT License

## 기여

기여를 환영합니다! Pull Request를 자유롭게 제출해 주세요.
