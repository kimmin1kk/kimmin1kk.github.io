---
title: "[Trouble Shooting] Spring Security 403 Forbidden 해결"
description: Spring Boot 3 버전 Spring Security를 사용하다 겪었던 문제와, 해결방안을 정리해 둔 글입니다.
date: 2023-07-30 23:59:00 +09:00
categories: [Trouble Shooting, Spring Boot, Spring Security]
pin : true
tags:
  [
    "403",
    Forbidden,
    Session & Cookie,
    SpringBoot,
    Authority
  ]
---

본 포스팅은 `Spring Boot 3.1.1` 기반으로 작성된 글이며,

인증 방식으로는 `Spring Security Session-Cookie` 방식을 사용했습니다.

# 문제 상황

토이프로젝트로 도서판매시스템을 개발하던 중.

myPage로 USER 권한이 있어야 들어갈 수 있게 했고,

회원가입을 하는 순간 USER 권한을 부여해줌.

그 이후 당연히 될 것 이라고 생각하고 myPage로 들어가는 순간!

`403 forbidden` 등장..

# 403 Forbidden?

> HTTP **`403 Forbidden`** 클라이언트 오류 상태 응답 코드는 서버에 요청이 전달되었지만, 권한 때문에 거절되었다는 것을 의미합니다.
>
>
> 이 상태는 `[401](https://developer.mozilla.org/ko/docs/Web/HTTP/Status/401)`과 비슷하지만, 로그인 로직(틀린 비밀번호로 로그인 행위)처럼 반응하여 재인증(re-authenticating)을 하더라도 지속적으로 접속을 거절합니다.
>

출처 : https://developer.mozilla.org/ko/docs/Web/HTTP/Status/403

# 조치 과정

1. ~~DB 데이터 확인 이후 데이터 입력은 문제가 없는 것을 확인 → 문제 X~~
2. ~~과정에서 누락된 로직이 있는 지 확인~~
3. **Slf4j를 통해 과정에서 권한이 누락되는 부분 확인**

   > user is User(seq=1, username=1, password=$2a$10$5Ib1OC2lG4Ar53tigrZ1ve3Ucao8pg.l6YB4m.HKzd93pfzX8ggim, name=1, nickname=1, grade=BRONZE, mileage=0, createdDate=2023-07-29 19:05:48.999699, modifiedDate=2023-07-29 19:05:48.999699, enabled=true, **authorities=[])**
   >

   **→ authorities가 빈 채로 넘어오는걸 발견**

4. 인증된 사용자의 권한 정보를 가져올 수 있게 함(UserServiceImpl → processRegistration 메서드 수정)
5. 메서드 수정 이후 무한 재귀 → `StackOverFlow` 예외 발생으로 인한 엔티티 수정
6. authorities가 정상적으로 넘어오는 것을 확인한 후 UserDetailsImpl 메서드 수정
7. 해결

# 변경된 소스코드 및 설정

- **들어가기 앞서, 시큐리티 설정(SecurityConfig)**

    ```java
    @RequiredArgsConstructor
    @Configuration
    public class SecurityConfig {
        private final CorsFilter corsFilter;
    
        @Bean
        public PasswordEncoder passwordEncoder() {
            return new BCryptPasswordEncoder();
        }
    
        @Bean
        public SecurityFilterChain filterChain(HttpSecurity httpSecurity) throws Exception {
    
            return httpSecurity
                    .formLogin(login -> login
                            .loginPage("/login") //User가 로그인 요청할 URL 지정
                            .defaultSuccessUrl("/", false)) //사용자가 인증되기 전에 방문하려고 한 페이지로 리다이렉트 됨
                    .logout(logout -> logout
                            .logoutUrl("/logout") //User가 로그아웃 요청할 URL 지정
                                    .logoutSuccessUrl("/") //로그아웃 성공 후 사용자가 리다이렉트 될 URL 지정
                                    .invalidateHttpSession(true) // 로그아웃 성공 시 사용자의 HttpSession 무효화 설정
                    )
                    .addFilterBefore(corsFilter, UsernamePasswordAuthenticationFilter.class) // CORS 필터를 UsernamePassword..필터 전에 추가해서 CORS 관련 처리가 등록된 필터보다 먼저 실행되게 함
                    .csrf(AbstractHttpConfigurer::disable) //개발할 때 CSRF에 대한 추가 설정 없이 테스트하기 위해 CSRF 보호 비활성화, 실제 배포할 경우에는 활성화 해두는게 좋음
                    .authorizeHttpRequests(registry -> { //
    
                        registry.requestMatchers("/myPage").hasRole("USER") //myPage URL 요청 -> 사용자 역할이 USER일 때만 허용됨
                                .requestMatchers("/", "/**").permitAll(); // root 및 모든 경로에 대한 모든 요청은 모든 사용자에게 허용
    
                    }).getOrBuild();
    
        }
    } 
    ```


- **인증된 사용자의 권한 정보를 가져올 수 있게 함 (UserServiceImpl)**


    before
    
    ```java
    @Override
        @Transactional
        public void processRegistration(RegistrationForm form)
            Authority auth = new Authority();
            auth.setRole(Role.ROLE_USER);
            auth.setUser(userRepository.save(form.toUser(passwordEncoder)));
            authorityRepository.save(auth);
        }
    ```
    
    after
    
    ```java
    @Override
        @Transactional
        public void processRegistration(RegistrationForm form) {
            Authority auth = new Authority();
            auth.setRole(Role.ROLE_USER);
            User newUser = form.toUser(passwordEncoder);
            auth.setUser(newUser);
            User savedUser = userRepository.save(newUser);
            savedUser.getAuthorities().add(auth);
            authorityRepository.save(auth);
        }
    ```


### 수정 후 StackOverflow 예외에 따른 변경

- Authority(Entity)


    Before
    
    ```java
    @Entity
    @Data
    public class Authority {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private long seq;
    
    		... 나머지 생략 ...
    }
    ```
    
    After
    
    ```java
    @Entity
    @Getter
    @Setter
    @EqualsAndHashCode(onlyExplicitlyIncluded = true) <-- 추가
    public class Authority {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        @EqualsAndHashCode.Include <-- 추가
        private long seq;
    
    		... 나머지 생략 ...
    }
    ```

- User(Entity)


    Before
    
    ```java
    @Entity
    @Data
    @EntityListeners(AuditingEntityListener.class)
    public class User {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private long seq;
    
    		... 나머지 필드 생략 ...
    
    }
    ```
    
    After
    
    ```java
    @Entity
    @Getter
    @Setter
    @EqualsAndHashCode(onlyExplicitlyIncluded = true) <-- 추가
    @EntityListeners(AuditingEntityListener.class)
    public class User {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        @EqualsAndHashCode.Include <-- 추가
        private long seq;
    
    		... 나머지 필드 생략 ...
    
    }
    ```


### authorities 확인 이후 UserDetailsImpl 수정


before

```java
@Override
    @Transactional
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities.stream()
                .map(authority -> (GrantedAuthority) () -> authority.getRole().toString())
                .collect(Collectors.toSet());
    }
```

after

```java
@Override
    @Transactional
    public Collection<? extends GrantedAuthority> getAuthorities() {
        log.info("UserDetailsImpl -> getAuthorities : OK");

        if (authorities.isEmpty()) {
            log.info("authorities is empty");
        }else {
            log.info("authorities size: {}", authorities.size());
        }
        return authorities.stream()
                .map(authority -> new SimpleGrantedAuthority(authority.getRole().name()))
                .collect(Collectors.toSet());
    }
```

# 마무리

스프링 시큐리티를 처음 도입한 토이프로젝트였지만 스프링 부트 3 버전을 사용해버리는 바람에 자료를 찾기 힘들어 간단해보이지만 주말내내 고생을 했습니다..

수정할 사항이나 추가해야할 사항이 있다면 댓글이나 이메일로 남겨주세요.
