# JungleTeamLog

> 정글의 모든 기록을 모으다

Krafton Jungle의 주차별 팀 활동과 학습 기록을 관리하기 위한 팀 기록 서비스입니다.

매주 팀이 새롭게 구성되고 핵심역량 목표, 일일 스크럼, 코어타임, WIL 등의 기록이 발생하는 환경에서 이를 주차별로 한곳에서 관리하고 다시 복기할 수 있도록 구현했습니다.

## 개발 기간

- 2026.08.24 ~ 2026.08.27
- 08.24 : 기획 발표
- 08.25 : MongoDB 구조 및 API 설계, 역할 분담, 프로젝트 구조 설계
- 08.26 : 기능 개발, 통합 테스트, 트러블슈팅, PPT 작성
- 08.27 : 배포 및 세부 기능 추가

## 주요 기능

### 1. 로그인 / 회원가입

- 회원가입 및 로그인
- JWT 기반 사용자 인증
- 로그아웃
- 인증된 사용자에 대한 접근 제어

### 2. 주차별 팀 관리

- 주차별 팀 생성
- 팀원 참여 관리
- 동일 주차 내 팀원 중복 참여 방지
- 주차별 팀 생성 여부 표시
- 팀에 참여한 사용자만 해당 팀 페이지에 접근 가능<img width="674" height="374" alt="스크린샷 2026-08-27 오후 2 26 55" src="https://github.com/user-attachments/assets/44a37c9a-460e-47c0-ae27-3dfcb782cc49" />


### 3. 팀 기록 관리

- 주차별 핵심역량 목표 등록
- 일일 스크럼 기록
- 코어타임 기록
- WIL 작성 및 조회
- 팀원별 WIL 조회

## 기술 스택

| Category | Technology |
|---|---|
| Backend | Flask |
| Database | MongoDB |
| Template Engine | Jinja2 |
| Authentication | JWT |
| Frontend | HTML, CSS, JavaScript, jQuery, Bulma |
| Web Server | Nginx |
| Deployment | AWS EC2 |

## 시스템 아키텍처
<img width="674" height="374" alt="스크린샷 2026-08-27 오후 2 26 55" src="https://github.com/user-attachments/assets/4063393f-c4bc-47e2-846d-8e3683a4145d" />

```text
Client
  │
  │ HTTP Request
  ▼
Nginx
  │
  ▼
Flask Server
  ├── Routing
  ├── Jinja2 Template Rendering
  ├── JWT Verification
  └── Business Logic
  │
  ▼
MongoDB
  ├── users
  ├── team_page
  ├── goals
  ├── scrums
  ├── coretime
  └── wil
