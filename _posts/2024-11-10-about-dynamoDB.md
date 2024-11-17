---
title: DynamoDB란?
description: 걸 쓰고 정리해보았읍니다.
date: 2024-11-10 23:50:00 +09:00
categories: [Study, AWS, DynamoDB]
pin : true
tags:
  [
    DynamoDB,
    NoSQL,
    AWS,
    ExclusiveStartKey,
    Pagination
  ]
---

## DynamoDB

DynamoDB는 AWS에서 제공하는 서버리스 기반 Key-Value 쌍으로 이루어진 NoSQL DB임.

---

## 특징

### NoSQL

- NoSQL DB는 `Join` 개념이 없음.
- 애플리케이션 레벨에서 구현할 순 있지만 매우 비효율적이며 NoSQL 쓰는 이유랑 맞지 않음.
- `Join` 개념이 없기 때문에 정규화가 불가능함.
- 보통 NoSQL에서는 반정규화를 통해 데이터를 처리함.
- RDBMS는 테이블을 나누는 방식으로 데이터를 관리하지만, DynamoDB에서는 모든 데이터를 하나의 테이블에 표현할 수 있음.

### HTTP 통신

- 대부분의 DB 리소스는 TCP Connection 기반이지만, DynamoDB는 `Connectionless`임.

### 서버리스

- DynamoDB는 별도의 서버가 존재하지 않고 온디맨드 방식으로 운영됨.

### Key-Value

- Key를 제외하고 테이블 속성을 미리 정의할 필요 없음.
- 미리 스키마를 정의하는 RDB와 달리 유연한 데이터 처리 가능.

---

## 사용하기 위한 지식 & 활용

DynamoDB는 NoSQL이라 스키마에 종속되지 않음.  
PK와 필요시 SK 정도만 정의하면 됨.

### 파티셔닝 원리 이해

- DynamoDB 내부에는 **해시 함수**가 존재.
- PK는 이 해시 함수를 통해 데이터를 저장할 **파티션**을 결정함.
- 동일한 파티션 키를 가진 데이터는 물리적으로 가까운 위치에 저장되며, 데이터를 구분하기 위해 SK를 사용.

![PK는 AnimalType, Name은 SK](https://github.com/user-attachments/assets/2e7321a3-79d6-428f-b30d-acd2e5cc2f49)
*PK는 AnimalType, Name은 SK*

**Partition Key (PK)**

- 데이터를 저장할 물리적 공간인 Partition을 구분하기 위한 키.
- 규모가 커져도 Address를 알고 있어 데이터를 빠르게 가져올 수 있음.

**Sort Key (SK)**

- Partition 내 데이터를 정렬하기 위한 키.
- Number, Binary, String 타입을 지원.
- 단순 정렬로 인해 Partition 크기가 커져도 데이터 검색 속도가 유지됨.

---

## Pagination

DynamoDB는 기본적으로 데이터를 페이지 단위로 반환하며, 이를 통해 대규모 데이터셋을 효율적으로 처리할 수 있음.

### Pagination을 왜 고려해야 할까?

대규모 데이터셋을 다루는 경우 모든 데이터를 한 번에 가져오는 것은 다음과 같은 이유로 비효율적일 수 있음:

1. **성능 저하**
    - DynamoDB는 **최대 1MB 크기의 데이터**를 반환할 수 있으며, 데이터가 많을수록 처리 시간이 길어짐.
    - 네트워크 트래픽 증가로 인해 클라이언트와 서버 간 통신 성능이 저하될 수 있음.

2. **비용 증가**
    - DynamoDB는 요청 수에 따라 비용이 청구됨. 대량의 데이터를 한 번에 가져오는 경우 비효율적인 요청이 발생할 수 있음.

3. **사용자 경험**
    - 프론트엔드에서 사용자가 볼 필요 없는 모든 데이터를 로드하면 UI 응답 속도가 느려질 수 있음.
    - Pagination을 통해 사용자에게 필요한 데이터만 점진적으로 제공 가능.

### Pagination 원리

1. DynamoDB는 각 쿼리 요청에 대해 최대 **1MB** 크기의 데이터를 반환.
2. 쿼리 결과가 **1MB를 초과**하면 응답 객체에 **`LastEvaluatedKey`**라는 속성이 포함됨.
3. 이후 페이지 데이터를 가져오려면, **`ExclusiveStartKey`**에 **`LastEvaluatedKey`** 값을 포함해 다음 요청을 보내야 함.

### ExclusiveStartKey란?

**`ExclusiveStartKey`**는 DynamoDB에서 다음 페이지 데이터를 가져오기 위해 사용하는 시작 지점을 지정하는 키입니다.  
이는 이전 응답에서 반환된 **`LastEvaluatedKey`** 값을 그대로 전달하는 형태로 동작합니다.

#### 특징
- **Key 기반 데이터 검색**: `ExclusiveStartKey`는 DynamoDB가 내부적으로 데이터 검색을 시작할 지점을 결정함.
- **연속된 페이징**: 이를 통해 데이터가 정확히 이어지며 중복이나 누락이 발생하지 않음.
- **유연한 요청 설계**: 필요한 데이터만 가져올 수 있도록 클라이언트와 연동 가능.

#### 동작 방식
- `LastEvaluatedKey`는 반환된 데이터의 마지막 아이템에 대한 파티션 키와 정렬 키 정보를 포함함.
- DynamoDB는 이 키를 기준으로 다음 데이터 검색을 시작.

## 주의사항

- DynamoDB의 쿼리는 **인덱스 설계**에 크게 의존함.
- 용량 모드와 보조 인덱스 사용 계획을 미리 세워야 함.



