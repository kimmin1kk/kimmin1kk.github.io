---
title: Entity 생명주기와 영속성 컨텍스트
description: Entity 생명주기와 영속성 컨텍스트에 관해 공부한 내용을 정리한 글입니다.
date: 2024-05-28 23:59:59 +09:00
categories: [Study, Spring Boot, JPA]
pin : true
tags:
  [
    JPA,
    Persistence Context,
    Entity Lifecycle
  ]
---

# 엔티티 생명주기
### 4가지 상태

- 비영속 (new/transient) - 영속성 컨텍스트와 전혀 관계가 없는 상태
    - 예시 (객체를 생성한 상태)

        ```java
        Member member = new Member();
        member.setId(100L);
        member.setUsername("회원1");
        ```

- 영속 (managed) - 영속성 컨텍스트에 저장된 상태
    - 예시 (객체를 저장한 상태)

        ```java
        em.persist(member);
        ```

- 준영속 (detached) - 영속성 컨텍스트에 저장되었다가 분리된 상태
    - 예시 (회원 엔티티를 영속성 컨텍스트에서 분리한 상태)

        ```java
        em.detach(member);
        ```

- 삭제 (removed) - 삭제된 상태
    - 예시 (객체를 삭제한 상태)

        ```java
        em.remove(member);
        ```


- 설명 사진
  ![](https://velog.velcdn.com/images/kimmin1kk/post/c22ac153-dcbd-4228-9b9f-0dd9ef213158/image.png)


# 영속성 컨텍스트

- **JPA 핵심 용어**
- 엔티티를 영구 저장하는 환경
- 애플리케이션과 DB 사이에서 객체를 보관하는 가상의 DB 역할을 함

## 특징

- 엔티티를 식별자 값으로 구분하기 때문에 **식별자 값**이 없으면 예외 발생
- EntityManager를 생성할 때 하나 만들어짐
- EntityManager를 통해 영속성 컨텍스트에 접근하고 관리할 수 있음

## 영속성 컨텍스트를 사용하는 이유 ( 장점 )
- **1차 캐시**
- 동일성(Identity) 보장
- 트랜잭션을 지원하는 쓰기 지연 (Transactional write-behind)
- **변경 감지(Dirty Checking)**
- 지연 로딩(Lazy Loading)

### 1차 캐시
JPA에서 1차 캐시 = EntityManager가 관리하는 영속성 컨텍스트 내부에 있는 첫 번째 캐시
캐시라는 말에서 알 수 있듯 데이터의 정보를 잠시 저장하는 역할을 해주기도 함
**1차 캐시를 이용함으로 인해 DB 조회 횟수를 줄일 수 있음**

>#### 1차 캐시의 조회 동작
1. 1차 캐시에 데이터가 있는지 확인. 있으면 가져옴 (PK로 비교)
2. 1차 캐시에 데이터가 없으면 DB에 데이터를 요청
3. DB에서 받은 데이터를 다음에 재사용 할 수 있도록 1차 캐시에 저장

### 동일성(Identity) 보장
같은 Transaction or 같은 EntityManager에서 가져온 객체는 항상 동일한 객체 리턴

### 트랜잭션을 지원하는 쓰기 지연 (Transactional write-behind)
한 Transaction안에서 이뤄지는 UPDATE나 SAVE 등의 쿼리를 쓰기 버퍼에 가지고 있다가 트랜잭션이 커밋되는 순간 한 번에 DB에 날리는 것
```java
transaction.begin();
em.persist(member1);
em.persist(member2);

// SQL 버퍼에 쿼리를 담은 상태

em.flush();

// 영속성 컨텍스트의 변경내용을 DB에 동기화

transaction.commit(); 

//버퍼의 쿼리가 DB에 넘어감
```


#### flush?
flush는 영속성 컨텍스트의 변경 내용을 DB에 반영하는 것
>#### 플러시 실행 시 일어나는 동작
1. 변경 감지 동작 -> 영속성 컨텍스트에 있는 모든 엔티티를 스냅샷과 비교. 수정된 엔티티 찾음
2. 수정된 엔티티는 수정 쿼리를 만들어 쓰기 지연 SQL 저장소에 등록
3. 쓰기 지연 SQL 저장소의 쿼리를 DB에 전송

#### Snapshot?
JPA는 엔티티를 영속성 컨텍스트에 보관할 때 최초 상태를 복사해서 저장해둠 -> Snapshot

> #### 영속성 컨텍스트 flush 하는 방법 3가지
1. em.flush() - 직접 호출
2. Transaction Commit - flush 자동 호출
3. JPQL 쿼리 실행 - flush 자동 호출


### 변경 감지(Dirty Checking)
영속 상태의 엔티티의 변경사항을 DB에 자동으로 반영하는 기능
```java
transaction.begin();

Member MemberA = em.find(Member.class, "MemberA");

memberA.setUsername("kimmin");
memberA.setAge("24");

transaction.commit();
// Update 해주는 코드가 존재하지 않아도 자동으로 반영
```

# 마치며
JPA 프록시 객체를 공부하기전 영속성 컨텍스트에 관한 정리를 하고 넘어가야 할 것 같아 구글링 및 교재를 참고해 글을 작성했습니다.
지연 로딩(Lazy Loading)에 관한 내용은 프록시 객체 관련 글을 올릴 때 정리하여 올릴 예정입니다.

수정할 사항이나 추가해야할 사항이 있다면 댓글이나 이메일로 남겨주세요.




