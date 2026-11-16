# AI Security Lab — 연구소 소개 홈페이지

기존 공격·방어·평가 실습을 보존하면서 독립된 `website/` 폴더에 추가한 정적 홈페이지입니다.

## 실행

저장소 최상위 폴더에서:

```bash
python3 -m http.server 8000 --directory website
```

브라우저에서 `http://127.0.0.1:8000`을 엽니다. Python 3.10 이상 외 별도 설치나 API 키가 필요하지 않습니다.

## 검증

```bash
python3 -m unittest discover -s website -p 'test_site.py' -v
```

검사: 페이지 섹션, 제목·접근성 기본 요소, 내부 링크, 외부 링크 보안 속성, 외부 리소스 부재, 모바일 대응, 개인정보 주의 문구.

**주의:** 위 자동검사는 정적 구조에 대한 회귀 검사입니다. 실제 Chrome·Edge 화면, 키보드 접근성, 모바일 렌더링 및 실습 Python 코드는 별도로 확인해야 합니다. 통과를 확인하지 않은 시험은 통과로 보고하지 않습니다.

## 내용과 범위

- 연구 분야 3개: AI 공격 분석 / AI 방어 기술 / 독립 성능 평가
- 연구 절차 4단계: 정의 / 설계 / 검증 / 기록
- 실제 `ai-security-lab-001` 저장소 실습 소개와 GitHub 링크
- GitHub 이슈를 이용한 협력 의견 접수
- 로그인, 개인정보 수집, API, DB, 외부 자바스크립트, 유료 서비스 없음

## 기존 파일 보존 및 재개

이 기능은 `website/` 안에만 신규 파일을 추가하며 `attacker/`, `defender/`, `evaluator/`, `scripts/`, `shared/`, `tests/`, `AGENTS.md`, 기존 `README.md`를 변경하지 않습니다.

작업 중단 시에는 다음 순서로 복구합니다.
1. `git status --short`로 변경 내용을 먼저 확인합니다. 수정 중인 파일이 있으면 덮어쓰지 않습니다.
2. `git branch --show-current`로 작업 브랜치를 확인합니다.
3. `python3 -m unittest discover -s website -p 'test_site.py' -v`를 실행합니다.
4. `python3 -m http.server 8000 --directory website`으로 브라우저 검증을 합니다.
5. 결과와 남은 문제를 PR에 기록한 후 검토합니다. 사용자 승인 없이 `main`에 병합하지 않습니다.

홈페이지는 **연구·실습 소개 시안**이며 특정 대학의 공식 홈페이지임을 주장하지 않습니다.
