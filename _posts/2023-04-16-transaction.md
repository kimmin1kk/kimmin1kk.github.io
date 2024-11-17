---
title: Transaction?
description: Transaction에 관해 공부한 내용을 정리한 글입니다.
date: 2023-04-16 23:59:00 +09:00
categories: [Study, Database, Transaction]
pin : true
tags:
  [
    Database,
    Transaction,
    ACID
  ]
---

# Transaction
DB의 상태를 변화시키기 위해 수행하는 가장 작은 작업의 단위.

## 특징 (A.C.I.D)
>
### 원자성 (Atomicity)
>> Transaction은 DB에 모두 반영되거나 모두 반영되지 않아야 함
쪼갤수 없는 가장 작은 단위 = 원자
>
###  일관성 (Consistency)
>> Transaction의 작업 처리 결과가 항상 일관성이 있어야 함
>
### 독립성 (Isolation)
>> 어떤 하나의 Transaction이라도, 다른 Transaction의 연산에 끼어들 수 없음
>
### 지속성 (Durability)
>> Transaction이 성공적으로 완료됐을 경우, 결과는 영구적으로 반영되어야 함
>

## 예시 (계좌이체)
>
### 과정
>
1. **구매자**의 계좌에서 돈이 **출금**됨
2. **판매자**의 계좌에 돈이 **입금**됨
>
### Query문
```
Update accounts
SET balance = balance - 10000
WHERE user = '구매자';
>
UPDATE accounts
SET balance = balance + 10000
WHERE user = '판매자';
```
### 예상 오류
+ 구매자의 돈이 출금됐는데 DB가 다운된 상황
+ 구매자는 돈을 보내지 않았는데 판매자에게 돈이 들어온 상황
+ 구매자와 판매자 사이에 출금과 입금이 전부 안되는 상황
>
**이러한 오류(어중간한 상황)을 없애기 위해 Transaction이 존재함.**

### Transaction 설정이 중요한 이유

> **DB 작업이 들어왔을 때 모든 작업의 독립성을 보장해 하나씩 순차적으로 진행할 경우**
>>
INPUT/OUTPUT 작업 속도 | CPU > DBMS
>>
Transaction을 순차적으로 작업하게 될 경우 CPU가 응답을 기다리는 시간은 점점 길어지게 됨. -> 프로그램이 비효율적으로 동작
>>
**DB에 저장된 무결성과 동시성의 성능을 지키기 위해 Transaction의 설정이 중요함**

## Transaction Mechanism
![](https://velog.velcdn.com/images/kimmin1kk/post/5896fef9-a8f4-47d0-8352-6b75f8a3e5fd/image.png)

## 사용
DB에서는 각각의 명령을 하나의 트랜잭션을 보고 보장해주기 때문에
여러 명령을 하나의 트랜잭션으로 묶고 싶은 경우에는 개발자가 직접 트랜잭션의 경계를 설정해줘야 함

### Spring에서 Transaction 경계설정
스프링은 트랜잭션 추상화 인터페이스인 PlatformTransactionManager를 제공
-> 다양한 DataSource에 맞게 Transaction을 관리할 수 있게 하고 있음
[PlatformTransaction Manager 인터페이스](https://velog.velcdn.com/images/kimmin1kk/post/be15eaed-2199-4462-a0cb-fb07213f5525/image.png)는 getTransaction, rollback, commit으로 구성

getTransaction 메서드를 통해 파라미터로 전달되는 TransactionDefinition에 따라 Transaction 시작. Transaction을 문제없이 마치면 commit, 문제가 발생하면 rollback 호출
-> Transaction 경계설정

#### 스프링이 제공하는 트랜잭션 구현체
+ DataSourceTransactionManager
    - for JDBC
+ JpaTransactionManager
    - for JPA
+ JtaTransactionManager

DataSourceTransactionManager와 JpaTransactionManager
하나의 DB사용 or 각각의 데이터를 독립적으로 사용하는 로컬 트랜잭션의 경우에 사용

JtaTransactionManager
하나 이상의 DB가 참여하는 경우 글로벌 트랜잭션의 경우에 사용
여러 개의 DB에 대한 작업을 하나의 트랜잭션으로 묶을 수 있음.
다른 서버에 분산된 것도 묶을 수 있음.

## 선언적 Transaction

### tx namespace
Bean 설정 파일에서 TransactionManager를 Bean으로 등록하고
속성과 대상을 정의해 Transaction을 적용하겠다고 명시하는 것

**코드에 영향 X, 일괄적으로 Transaction을 적용할 수 있다는 장점이있음 **

### @Transactional
@Transactional은 Method, Class, Interface 등에 적용할 수 있음

중첩되어 존재하는 경우
Class Method - Class - Interface Method - Interface순으로 우선순위를 갖고 적용

@Transactional은 통상적으로
DB에 여러번 접근하면서 하나의 작업을 수행하는 Service 계층 메서드에 붙임

**세밀한 설정을 손쉽고 간편히 할 수 있다는 장점이 있음**

#### @Transactional - propagation = 전달받는 Transaction 전파
Transaction의 경계에서 이미 진행중인 Transaction이 있을 때 어떻게 동작할지 결정하는 것

|속성| 설명 (Tra=Transaction)|
|-|-|
|REQUIRED|(Default) 진행중인 Tra1이 있다면 Tra1 참여, 없으면 Tra1 시작. 어느 메서드에서 문제가 발생해도 모든 메서드가 롤백이 됨|
|SUPPORTS|진행중인 Tra1이 있으면 참여. 없으면 Tra 없이 메서드를 그냥 실행|
|MANDATORY|Tra1이 있으면 참여, 없으면 예외 발생|
|REQUIRES_NEW|항상 Tra 시작, 새로운 메서드2가 시작되었을 때 기존에 진행중인 Tra1을 보류시키고 Tra2 시작|
|NOT_SUPPORTED|이미 시작된 Tra1이 있다면 Tra1을 보류하고 자신의 메서드 실행(Tra 사용 X)|
|NEVER|Tra 사용하지 않도록 강제함. 이미 진행중인 Tra 없음 -> 자신의 메서드 실행 / Tra 있음 -> 예외 발생|
|NESTED|이미 진행중인 Tra1이 있으면 그 안에 새로운 Tra2 삽입. 부모인 Tra1의 커밋, 롤백에는 영향 O / Tra2의 커밋, 롤백에 Tra1은 영향 X|

#### @Transactional - isolation = 전달받는 Transaction 격리수준
동시에 여러 Tra가 실행될 때, Tra 작업 내역을 다른 Tra에 보여줄지 말지 결정 가능한 많은 Tra를 동시에 진행하면서도 문제가 생기지 않도록 하려는 설정 기본적으로 DB에 설정되어 있지만 이 속성을 통해 재설정 할 수 있음

|속성| 격리수준 |설명 (Tra=Transaction)|
|-|-|-|
|DEFAULT|가장 낮은 격리수준|DB의 기본 설정을 따름, 대부분의 DB는 READ_COMMITTED를 기본 격리수준으로 갖고있음.|
|READ_UNCOMMITTED|가장 낮은 격리수준, | 아직 커밋되지 않은 데이터를 다른 Tra이 읽을 수 있음 Tra1에서 Tra2로 데이터를 읽어 오다가 Tra1 실행 중 문제가 발생해 Rollback 될 경우, Tra2는 존재하지 않는 데이터를 불러오는 문제가 발생할 수 있음|
|READ_COMMITTED|두번째로 낮은 격리수준|가장 많이 사용됨. 커밋되지 않은 정보는 읽어올 수 없음 Tra1에서 작업이 완료되어 커밋 되어야지만 Tra2가 읽어올 수 있음. 하지만 Tra3가 Tra2 값을 또 수정할 수 있어 Tra2가 다시 읽으면 값이 다른 문제가 발생할 수 있음|
|REPEATABLE_READ|세번째로 낮은 격리수준|하나의 Tra이 읽은 로우를 다른 Tra에서 수정할 수 없게 함. 하지만 기존에 user1만 있던 DB를 Tra1이 조회해 user1이라는 로우를 얻었는데 Tra2가 user2라는 새로운 로우를 추가한느 것은 제한되지 않아 다시 조회했을 때 발견하지 못한 새로운 로우가 발견되는 문제가 발생할 수 있음 |
|SERIALIZABLE|마지막 격리수준(가장 강력한 격리수준)|이 속성을 가진 Tra가 있으면 동시에 같은 Table의 정보를 접근할 수 없음. 하지만 Tra를 순차적으로 수행하는 것과 같으므로 성능이 매우 떨어짐. -> 극단적인 상황에만 사용하는걸 권장|

#### @Transactional - timeout = 지정되는 Transaction 제한시간
초 단위로 제한시간을 지정할 수 있음.
따로 설정하지 않으면 timeout은 지정되어 있지 않음

#### @Transactional - readOnly = 읽기전용 Transaction
True로 설정
- Update, Insert, Delete 작업을 방지
- flush모드가 manual로 설정됨. (jpa의 더티체킹 기능을 무시할 수 있음)
  기본값은 False (모든 작업 허용)

#### @Transactional - rollbackFor = 전달받는 Transaction 롤백 예외
기본적으로 Transaction은 런타임 Exception, 에러 발생시에만 롤백함
하지만, 체크예외나 예외가 발생하지 않으면 커밋하도록 함
체크 예외를 롤백 대상으로 삼고 싶으면 특정 Exception을 클래스로 전달해 사용할 수 있음
```
//Example
@Transactional(rollbackFor=NoSuchElementException.class)
-> NoSuchElementException에 대해 예외 발생시 롤백
```
#### @Transactional - noRollbackFor = 전달받는 Transaction 커밋 예외
위의 rollbackFor 개념과 반대라고 생각하면 됨
```
//Example
@Transactional(noRollbackFor={IOException.class, SqlException.class})
-> 런타임 예외인 IOException이나 SqlException 예외 발생시 롤백 대상인 두 예외를 롤백하지 않고 커밋
```

# 마치며
이번 글은 JPA를 사용하면서 @Transaction 어노테이션을 사용할 때
아주 간단하게 잘 되면 커밋. 오류 발생 시 롤백 정도로만 알고 사용하다가 좀 더 알고 싶어서 공부 하게 되었고 테코톡 유튜브에 정리가 잘 되어 있는 거 같아 참고하면서 글을 작성했습니다.

아래는 글을 작성하면서 참고했던 링크입니다.
[[10분 테코톡] 🐤 샐리의 트랜잭션](https://www.youtube.com/watch?v=aX9c7z9l_u8)
[[10분 테코톡] 🙊 에이든의 트랜잭션 메커니즘](https://www.youtube.com/watch?v=ImvYNlF_saE)

수정할 사항이나 추가해야할 사항이 있다면 댓글이나 이메일로 남겨주세요.

