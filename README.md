# 제주도 옥상 우수량 산정기

합리식(Rational Method) 기반 옥상 첨두유량 산정 웹 앱.  
제주특별자치도 하수도정비 기본계획 Talbot형 강우강도식 적용.

## 기능

- 지붕 유형별(콘크리트·녹화 등) 면적 개별 입력 → 가중 유출계수 자동 산정
- 건물 용도 → 설계빈도 자동 결정 (10·30·50·100년)
- 합계 면적 기반 강우 지속시간 자동 추천
- **상층 벽면 우수** 포함 (고층 건물 옥상정원 적용)
- 배관 방식별(수직 낙수관·수평 경사관·혼합·꺾임) 관경·개수 산정
- 전체 관경 클릭 선택 및 여유율 표시

## 로컬 실행

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# http://localhost:8000 접속
```

## Railway 배포

1. 이 레포를 GitHub에 push
2. Railway → New Project → Deploy from GitHub Repo
3. 환경변수 설정:
   - `ALLOWED_BLOG` = 본인 블로그 도메인 (예: `myblog.tistory.com`)
   - 설정 안 하면 전체 공개

## 블로그 임베드 방법

```html
<!-- 블로그 포스트에 삽입 -->
<iframe 
  src="https://your-app.railway.app" 
  width="100%" 
  height="900"
  frameborder="0"
  style="border-radius:12px;">
</iframe>
```

## 기술 스택

- **Backend**: FastAPI + Uvicorn
- **Frontend**: Vanilla JS (단일 HTML)
- **배포**: Railway
- **접근 제어**: HTTP Referer 헤더 기반 블로그 도메인 화이트리스트

## 적용 기준

| 항목 | 기준 |
|------|------|
| 강우강도식 | 제주도 하수도정비 기본계획 (Talbot형) |
| 수직관 용량 | KDS 57 60 00, 만관 1/3 충만 기준 |
| 수평관 유량 | Manning 공식, 만관 기준 |
| 벽면 유효면적 | H × P × 노출비율 |

> 본 앱은 설계 참고용이며 실제 설계 시 최신 제주도 기본계획 확인 필요.
