---
title:  "[Trouble Shooting] Lambda 함수와 API Gateway 커스텀 도메인 연결"
description: 개발하면서 겪은 문제를 기록하고 해결 과정을 공유
date: 2024-11-15 00:19:32 +09:00
categories: [ Trouble Shooting, AWS ]
pin: true
tags:
  [
    Route 53,
    API Gateway,
    Lambda,
    Serverless
  ]
---

## 문제 상황

기존에는 `serverless deploy`로 생성된 endpoint를 프론트에서 하드코딩해서 사용했음.  
하지만 이 방식은 다음과 같은 문제가 있었음:

- `.env` 파일을 사용해 환경변수를 관리하려면 팀원들과 변경사항을 공유하고 통합하는 과정이 번거로움.
- CI/CD 환경에서 Github Secrets를 활용하면 로컬에서 테스트할 때 다시 설정을 맞추는 번거로움이 발생.

이를 해결하기 위해 **API Gateway를 커스텀 도메인에 연결**하는 방식을 도입함.

---

## 1. AWS Certificate Manager를 통한 인증서 생성

커스텀 도메인을 사용하려면 먼저 HTTPS를 위한 인증서가 필요함. AWS Certificate Manager를 사용하여 인증서를 생성함.

1. AWS Management Console에서 **Certificate Manager**로 이동.
2. 인증서를 요청(Request a Certificate) 버튼 클릭.
3. **Public Certificate** 옵션 선택 후 사용할 도메인 이름 입력.
    - 예: `api.example.com`
4. DNS 검증(DNS Validation)을 선택하고 다음 단계로 진행.
5. 검증을 위한 CNAME 레코드를 제공받음. 이를 **Route 53**의 해당 도메인에 추가.
6. 인증서 상태가 **Issued**로 변경되면 성공.

> **참고**: 인증서 발급에는 시간이 걸릴 수 있음.  
> 발급 후 API Gateway와 연결 가능.

---

## 2. API Gateway에 Custom Domain 연결

1. **API Gateway** 콘솔로 이동.
2. 왼쪽 메뉴에서 **Custom Domain Names** 선택 후 **Create** 버튼 클릭.
3. 다음 항목들을 입력:
    - **Domain Name**: 생성한 도메인 이름 (예: `api.example.com`)
    - **ACM Certificate**: 이전 단계에서 발급받은 인증서 선택.
4. Custom Domain Name 생성 후, **API Mappings**로 이동.
5. 다음과 같이 매핑 설정:
    - 기존 API 선택 (예: `Lambda API`)
    - Stage: `dev` (혹은 사용할 Stage)
    - Path: `/` 또는 `/v1` 등 원하는 경로 설정.

> **참고**: Path 설정 시 중복되지 않도록 주의.  
> 기존 API Gateway의 경로와 겹치지 않도록 Path를 설계해야 충돌을 방지할 수 있음.

---

## 3. Route 53에서 레코드 생성

도메인 이름을 실제로 사용할 수 있도록 **Route 53**에서 레코드를 생성해야 함.

1. **Route 53** 콘솔로 이동 후 도메인 선택.
2. **Create Record** 클릭 후 다음을 설정:
    - **Record Type**: A (Alias)
    - **Alias Target**: Custom Domain Name의 Regional API Gateway 엔드포인트 선택.
    - **Name**: 서브도메인 (예: `api`)

3. 레코드 생성 후, 브라우저에서 도메인으로 요청하여 API가 정상 작동하는지 확인.

---

## 결과

설정 완료 후 기존 URL:

```   https://asdfadsfad.execute-api.{region}.amazonaws.com/dev/files/presigned-url ```

은 커스텀 도메인으로 변경됨:

```      https://api.example.com/dev/files/presigned-url     ```

---

## 주의할 점

- **Path 중복 방지**:  
  API Gateway의 Path와 Custom Domain Path가 중복되지 않도록 설정해야 충돌 방지 가능.  
  예를 들어, API Gateway Path를 `/presigned-url`로 설정하고, Custom Domain Path를 `/dev/files`로 지정하는 방식으로 해결.

- **DNS Propagation**:  
  Route 53에서 레코드를 생성한 후 DNS 전파 시간이 필요할 수 있음. 설정 후 즉시 반영되지 않으면 조금 기다려야 함.

---

Lambda 함수와 API Gateway를 커스텀 도메인으로 연결하는 과정을 정리함.  
앞으로 API URL 관리와 팀원 간 협업이 더 편리해질 것으로 기대됨.

### 도움이 되셨길 바랍니다! 😀
