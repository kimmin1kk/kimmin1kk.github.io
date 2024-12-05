---
title:  "[Trouble Shooting] Resource handler returned message: 'Code Storage limit exceeded.'"
description: Serverless 프레임워크 배포 중 발생한 문제와 해결 과정을 공유
date: 2024-12-05 10:26:00 +09:00
categories: [ Trouble Shooting, AWS, Serverless ]
pin: false
tags:
  [
    AWS Lambda,
    Serverless,
    Storage Management,
  ]
---

## 문제 상황

Serverless Framework를 이용하여 서비스를 배포하던 중, 다음과 같은 오류가 발생함:

> CREATE_FAILED: UploadFileLambdaVersionBh5j5jxy3VYKXNWTOBwz5Z2JLV7vnxjvV50uJu30Ms (AWS::Lambda::Version) Resource handler returned message: "Code storage limit exceeded. (Service: Lambda, Status Code: 400, Request ID: 12102694-eb99-478b-8835-337bce31b17a)" (RequestToken: 837036e1-05cc-9142-1150-177c12125ac9, HandlerErrorCode: GeneralServiceException)

이 오류는 AWS Lambda의 코드 저장 용량 한도를 초과했음을 나타냄.  
기존 배포된 Lambda 함수와 버전들이 누적되어 AWS 계정당 75GB로 제한된   
**Code Storage Limit**을 초과했기 때문에 발생한 문제임.

---

## 원인 분석

Serverless Framework는 새로운 배포마다 Lambda 함수의 새로운 버전을 생성함.  
하지만 과거에 생성된 Lambda 버전들이 삭제되지 않고 남아 있는 경우, 제한된 저장 공간을 모두 차지하게 되어 배포가 실패함.

> AWS Lambda는 계정당 75GB의 코드 저장 공간을 제공하며, 이 한도를 초과하면 추가로 코드를 업로드할 수 없게 됨.

---

## 해결 방법

이 문제를 해결하기 위해 **Serverless Prune Plugin**을 사용하여 불필요한 Lambda 버전을 자동으로 정리(Prune)하도록 설정함.

1. **Serverless Prune Plugin 설치**

   ```bash
   npm install --save-dev serverless-prune-plugin
   ```

2. **serverless.yml 설정 추가**

serverless.yml 파일에 다음과 같이 설정:

```yaml
plugins:
- serverless-prune-plugin

custom:
  prune:
    automatic: true
    number: 3
```
automatic: true: 배포 후 자동으로 오래된 Lambda 버전을 삭제.   
number: 3: 최신 3개의 Lambda 버전만 유지하고 나머지는 삭제.

3. **배포 실행**

위 설정을 적용한 후 serverless deploy 명령어를 다시 실행.  
오래된 Lambda 버전들이 삭제되면서 저장 공간이 확보되고 배포가 정상적으로 완료됨.


## 왜 문제가 해결되었는가?
Serverless Prune Plugin을 사용하여 과거 배포로 인해 누적된 Lambda 버전을 정리함으로써, AWS Lambda의 코드 저장 공간이 확보되었음.  
결과적으로 새로운 Lambda 버전을 생성할 공간이 생겼고, 배포가 성공적으로 이루어짐.  

## 결론
Serverless Framework를 사용하여 AWS Lambda를 배포할 때는 저장 공간 관리가 중요함.  
오래된 Lambda 버전을 자동으로 삭제해주는 Serverless Prune Plugin을 설정하면, 저장 공간 초과 문제를 사전에 방지할 수 있음.  
   
팁: 정리할 Lambda 버전의 개수는 프로젝트에 따라 적절히 조정할 것.  
너무 적은 개수로 설정하면 이전 버전의 확인이 어려울 수 있음.  

### 도움이 되셨길 바랍니다! 😀
