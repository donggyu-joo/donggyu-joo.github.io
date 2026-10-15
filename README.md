# Donggyu Joo — personal website

- Website: https://donggyu-joo.github.io/
- Repository: https://github.com/donggyu-joo/donggyu-joo.github.io
- Maintainer account: `jdg10126`; organization: `donggyu-joo`.
- GitHub Pages deploys the committed files from `main`, repository root.

## 다른 컴퓨터에서 수정하기

Git과 Python 3를 설치하고, 저장소에 쓰기 권한이 있는 GitHub 계정으로 인증합니다.

```sh
git clone https://github.com/donggyu-joo/donggyu-joo.github.io.git
cd donggyu-joo.github.io
```

이미 내려받은 컴퓨터에서는 수정하기 전에 `git pull --ff-only`로 최신 내용을 받습니다.

| 수정할 내용 | 원본 파일 |
| --- | --- |
| 소개, 경력, 학력, 섹션 구성과 공통 HTML | `scripts/build.py` |
| 폰트, 색상, 크기, 간격, 반응형 배치 | `assets/style.css` |
| 논문 정보와 링크 | `data/publications.json` |
| 특허 정보와 링크 | `data/patents.json` |
| Scholar 인용수와 확인 날짜 | `data/scholar-citations.json` |
| 다운로드용 CV | `assets/CV_DonggyuJoo.pdf` (제공받은 원본 PDF) |

수정 후 HTML을 다시 생성합니다. HTML 빌드에는 Python 표준 라이브러리만 사용합니다.

```sh
python3 scripts/build.py
```

Windows에서 `python3` 명령이 없으면 `python` 또는 `py`를 사용합니다.
`index.html`, `publications.html`, `patents.html`, `404.html`은 생성 결과이므로
직접 수정하면 다음 빌드 때 덮어써집니다. 원본 스크립트 또는 JSON을 수정하세요.
HTML 빌드는 자동 배포 과정에서 실행되지 않으므로, 생성된 HTML도 함께 커밋해야 합니다.

## 미리보기와 배포

빌드 후 `index.html`을 브라우저에서 열어 데스크톱과 모바일 폭으로 확인할 수 있습니다.
별도 서버 없이 동작합니다. 선택적으로 로컬 서버를 쓸 수도 있습니다.

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

브라우저에서 http://127.0.0.1:8765 를 열고, 확인이 끝나면 터미널에서 `Ctrl+C`로 종료합니다.

```sh
git diff --check
git diff
git add scripts data assets index.html publications.html patents.html 404.html README.md .gitignore
git commit -m "Update website"
git push origin main
```

Push하면 GitHub Pages가 다시 배포합니다. 저장소의 **Actions** 탭에서 배포 성공을 확인한 뒤
실제 사이트를 새로고침하세요. 캐시가 남으면 강력 새로고침을 사용합니다.

## 다운로드용 CV

`assets/CV_DonggyuJoo.pdf`는 사용자가 제공한 원본 PDF의 디자인을 유지하며,
요청에 따라 O-1 비자 문구, 인용수 요약, 모델 크기·데이터 규모·성능 개선 수치만 제외한 버전입니다.
상용화 8건, 6명 리딩, 경력·학력·논문·수상·특허는 원본 내용을 유지합니다.
새 CV를 반영할 때는 이 파일을 공개할 PDF로 교체하고 커밋·push하면 됩니다.
HTML 빌드는 PDF를 생성하거나 수정하지 않습니다.
홈페이지의 경력·학력은 `scripts/build.py`에서 별도로 관리합니다.

Scholar 인용수는 2026-10-14에 확인한 스냅샷이며 자동 갱신되지 않습니다.
날짜 표시는 `scripts/build.py`에도 있으므로 인용수 갱신 시 함께 수정합니다.
추가 개인정보, 회사 내부 자료, 인증 정보는 이 공개 저장소에 넣지 않습니다.

## 방문 통계 (GoatCounter)

`data/analytics.json`의 `goatcounter_site_code`에 가입 후 발급받은 사이트 코드를 넣습니다.
예를 들어 대시보드 주소가 `https://example.goatcounter.com`이면 값은 `example`입니다.
빈 문자열이면 분석 스크립트를 넣지 않습니다.
코드 변경 후 `python3 scripts/build.py`로 HTML을 생성하고 함께 커밋·push합니다.

모든 페이지의 방문과 CV 다운로드 링크 클릭을 집계합니다.
`cv-download`는 링크 클릭 이벤트로, 파일 다운로드 완료를 의미하지는 않습니다.
통계는 GoatCounter 대시보드에서 확인하며 사이트 화면에는 카운터를 표시하지 않습니다.
비밀번호와 API 키는 사이트 코드에 필요하지 않으며 저장소에 넣지 않습니다.
통계를 비공개로 유지하려면 GoatCounter의 공개 대시보드 옵션을 끕니다.
본인 방문 제외 방법: https://www.goatcounter.com/help/skip-dev
