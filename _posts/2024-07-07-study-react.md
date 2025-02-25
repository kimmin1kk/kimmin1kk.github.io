---
title: Node.js / React 개념 정리
description: React 를 사용하기 전 개념 정리한 부분입니다.
date: 2024-07-07 17:18:18 +09:00
categories: [Study, Javascript, React]
pin: false
tags:
  [
    Node.js,
    React,
    Virtual Dom,
    Vite,
    Component,
    JSX
  ]
---

# Node.js

- 자바스크립트 런타임.
- Node.js 나오기 전까지는 자바스크립트 실행은 브라우저 기반임.
- 현재는 어떤 곳에서도 실행이 가능함. -> 대중화의 밑거름

## 개발 방법

- 모듈과 모듈 시스템의 개념으로 개발을 진행.
    - 모듈 : 재사용이 가능한 형태의 소스나 파일. 따라서, 재사용할 수 있는 모듈들이 모여서 하나의 시스템.
- React 에서도 모듈 기반의 개발을 진행하게 됨.
    - 앞으로 사용하게 되는 것은 ES(ECMAScript) 모듈 시스템으로 사용하게 됨.
    - package.json 에서 type 을 module 로 설정.

## 재사용성 ↑

- export 키워드를 사용해서 외부에서 사용될 수 있도록 공유.

- 관련 있는 기능이나 정보들은 하나의 javascript 파일에서 관리하게 됨.
  SRP 가 적용된 것과 동일

- 사용될 곳에서는 공유된 것을 import 해서 사용해야 함.
  import * as circle from "./circle.js";

- import 종류
    - 개별 내보내기 : export 를 함수명, 상수 앞에 붙여서 사용

    - 개별 불러오기 : import {함수명} from ...

    - 전부 불러오기 : import * from ...

    - 기본값으로 보내기 : export 와 함께 default 키워드 사용. <br/>
      기본값으로 보내기를 하면 불러올 때 중괄호를 사용하지 않아도 됨. 그리고, 자유롭게 이름을 지정해서 사용할 수 있음.


## 라이브러리 사용

- 외부 패키지(라이브러리)를 설치해서, 사용.
  ex) Lodash : 배열 및 객체를 다루는 데 특화된 기능을 제공하는 라이브러리.
- 설치 명령어
  npm i lodash (npm : node package manager, i : install)

# React

- Node.js 라이브러리

## 특징

- 컴포넌트 기반의 유연성 ( 기존 웹 페이지와 VS 컴포넌트 )
- 쉽고 간단한 업데이트 ( 선언형 프로그래밍 )
- 빠른 업데이트 ( Virtual DOM )

### 컴포넌트 기반의 유연성 ( 기존 웹 페이지와 VS 컴포넌트 )

```markdown
Header 가 모든 웹페이지에 포함되는 것을 가정.
웹페이지가 100개, 한 군데에서 Header 를 수정, 99군데를 수정해야 함.

Header 와 같은 재사용이 가능한 부분을 컴포넌트로 작성.
하나의 Header 컴포넌트로 모든 페이지에서 사용이 되도록 함. (React)

수정이 발생 하더라돠 하나의 컴포넌트만 수정하면, 모든 페이지에 반영이 됨.

컴포넌트는 함수 형태로 구현해서 호출해서 사용함.
호출해서 반환되는 값은 Header 태그가 반환됨. => React component
```

### 쉽고 간단한 업데이트 ( 선언형 프로그래밍 )

```markdown
- javascript
    - 개발자 주도 프로그래밍.
      명령형 프로그래밍 ( 개발자가 처음부터 끝까지 모두 구현 )
      모든 과정 하나하나를 설명. 코드가 길어지고 복잡해짐.
- React
    - 선언형 프로그래밍 ( 컴포넌트는 재사용, 함수 호출하듯이 사용 )
      Header 자리에 후보군이 3개가 있다고 가정.
        - Header1 : 1
        - Header2 : 2
        - Header3 : 3
        - state 변수( 컴포넌트 )를 1,2,3 중에 하나로 설정 (선언)
            - 해당되는 Header 가 화면에 적용되어 표시됨.
            - 화면 제어가 간편해짐.

        - 컴포넌트 기반의 화면 제어를 React 가 제공함.
```


## 자바스크립트 객체

1. 객체의 종류

- 내장 객체 - javascript 에서 미리 객체 정의되어 있는 API. <br/>
  개발자가 쉽게 사용할 수 있도록 미리 만들어진 객체
  ex) windows 객체
- DOM 객체
  document 객체

- 웹 브라우저 객체
  location, history 등의 객체

- 사용자 정의 객체

2. DOM (Document Object Model)

   - javascript 같은 프로그래밍 언어로 웹 문서에 접근하고 <br/>
     제어할 수 있도록 `웹 문서를 체계적으로 정리`하는 방법
   - DOM 에서는 웹 문서를 하나의 객체로 정의하고, 웹 문서를 이루는 <br/>
     모든 요소(Tag, Node)를 각각의 객체로 정의해서 관리.
   - DOM tree (DOM node tree) <br/>
     document - html - head and body - ...
   - document node
       - DOM tree 의 최상위 root node 임.
       - Html 문서당 document 객체는 하나. `유일함`
       - DOM 트리의 node 들에 접근하기 위한 진입점.
       - 전역 객체 window 의 document property 프로퍼티에 바인딩 되어 있음.

3. DOM 에서 node ( 웹 요소, tag )에 접근 - 제공해주는 API 를 사용.

4. Node(요소, tag) List

5. 노드 추가 및 수정을 위해서 제공되는 함수 (API)

6. document 객체(DOM)에 img tag(Node) 를 추가하는 사례

   - img tag 를 요소 노드로 신규 생성.
       - let newImg = document.createElement("img");
   - img tag 의 src 속성을 설정하기 위해서 속성 node 를 신규로 생성해야 함.
       - let srcNode = document.createAttribute("src")
       - srcNode.value = "images/wall.jpg";
   - 이제 이 둘을 연결해줘야 함. img tag 의 node 속성 node 연결
       - newImg.setAttribute(srcNode) <br/>

   ============== img tag node 구성 ===================== <br>

   - html 문서에서 img tag 와 연결될 부모 노드에 연결.
       - => 완성된 html 문서가 됨.
           - document.body.appendChild(newImg);
   
   ============== html document 구성 완료 ================

### 빠른 업데이트 ( Virtual DOM )
```markdown
- 브라우저 화면 업데이트 단계
    - ( HTML, CSS ) -> 렌더 트리 -> 레이아웃 -> 페인팅
    - 렌더 트리 : DOM 과 CSSOM 적용
    - 레이아웃 : DOM 정보를 바탕으로 화면(모니터)상의 위치 정보(px)를 계산
    - 페인팅 : document 의 요소를 화면에 실제로 출력.

- Virtual DOM 을 활용해서 document 의 수정, 추가, 삭제와 관련된
  모든 변경 사항을 브라우저의 DOM 에 적용하지 않고,
  React 의 Virtual DOM ( 브라우저 DOM 의 복사본 )에 적용하고,
  적용이 완료되면, 한 번에 브라우저 DOM 에 적용하는 방법으로
  렌더링 속도를 개선함.
``` 

### create React app VS vite
    vite 가 create React app 보다 최신

    둘 다 React 프로젝트를 빠르게 시작하고 간단하게 설정을 제공

    성능과 다양한 커스터마이제이션은 vite가 더 우수함.
    vite 는 더 빠르고, 유연한 개발이 되도록 지원하며, React 와 다른 프레임워크를 위한 범용 도구로도 사용가능.

    따라서, 실습은 vite 로 진행.

###  React 프로젝트 생성 및 React app 실행

    1 프로젝트 생성 with vite(비트)
        npm create vite@latest

    2 생성된 프로젝트의 라이브러리 설치
        의존관계의 라이브러리를 일괄 설치

        npm install

    3 React app 실행
        npm run dev

        React app 실행이 되면, 기본적으로 웹 서버가 탑재되어 있음.

    4 프로젝트 구성
        - node_modules
          외부 라이브러리 설치 폴더
        - src
          프로젝트 관련 모듈을 관리하는 폴더

          *.jsx 는 javascript 로 구현해야 하는 컴포넌트 파일
          index.html 는 메인 화면. ( main.jsx 를 참조 )

## 컴포넌트 작성
### 컴포넌트
        html tag 를 반환하는 함수.
        ex) function App =>App 컴포넌트
### 컴포넌트 Header, Main, Footer 추가
        함수 선언 형태 / 화살표 함수로 컴포넌트를 생성.

        클래스로도 만들 수 있음. but 작성해야 할 코드가 너무 많아서, 개발 생산성이 나오지 않음.
        함수 형태로 컴포넌트를 만드는 것이 훨씬 일반적임.

        == 주의사항 ==
        함수 선언할 때 앞 글자 소문자로 하면 React 내부에서 컴포넌트로 인식하지 않음.

### 컴포넌트 사용

    <Header /> 와 같은 tag 형태로 컴포넌트를 호출해서 사용.

### 컴포넌트 간의 관계

    header 컴포넌트는 다른 컴포넌트인 App 컴포넌트에 포함되어 있음.

    header 컴포넌트는 App 컴포넌트의 자식 컴포넌트.

    현재의 컴포넌트들이 화면에 렌더링 되기 위해서는
    App 컴포넌트의 자식 컴포넌트로 존재해야 함.

    main.jsx 의 render 함수에 사용되는 컴포넌트가
    최상위(root) 컴포넌트가 됨.

    App( React app의 root 컴포넌트, Header 의 부모 컴포넌트 )

    일반적으로 Root 컴포넌트를 App 이라는 이름으로 컴포넌트를 설정해서 사용하는 것이 관례임.

### 컴포넌트 분리

    App.jsx 에 작성한 컴포넌트들을 별도의 파일로 작성 => 모듈화 시스템을 위해서
    컴포넌트별로 각각 파일을 나눠서 작성하는 것이 일반적임.

    - components 폴더
    - 3가지의 컴포넌트 파일을 생성
    - export(공유), import(참조) 추가
    - 3가지 컴포넌트에 대해서 import 할 때 명시적으로
      파일명을 작성하지 않았음.
      vite로 만든 앱에서는 확장자를 사용하지 않아도, 자동으로 파일을 찾아감. 내부적으로 설정이 되어있음.

### JSX( Javascript Extensions ) : 확장된 자바스크립트의 문법

    - JavaScript 함수로 html 을 반환
    - 컴포넌트 내에서 변수를 설정해서 html로 렌더링.
    - 변수 설정
      {number}

    중괄호 안에는 숫자나 문자열 값으로 평가가 될 수 있는 식이라면,
    무엇이든지 모두 사용 가능함.
    - JSX 의 주의 사항

      a. 중괄호 내부에는 자바스크립트 표현식만 넣을 수 있음.
         한 줄의 코드가 특정한 값으로 평가가 될 수 있는 식.
         따라서, 조건문, 반복문을 사용하면 오류가 발생하게 됨.

      b. 숫자, 문자열, 배열 값만 렌더링 됨.

      c. 객체의 경우, 프로퍼티를 지정해서 사용해야 함.

      d. 모든 태그는 닫혀 있어야 함.
         예로, <h1> 로 열면 반드시 </h1> 로 닫든지
         self closing 해줘야 함.

      e. 최상위 태그는 반드시 하나이어야 함.
         컴포넌트 내에서 태그는 최상위 레벨의 경우는 하나이어야 함.
         <main> 와 동일한 레벨의 <div> 태그가 있으면 안된다는 뜻.

         <main> 처럼 특정한 태그로 감싸줄 필요가 없는 경우.
         비어 있는 태그( <> </> )를 사용하면 됨.

### 컴포넌트에 값 전달
    Button 컴포넌트를 사용해서 4개를 렌더링했지만,
    구별이 되지 않는 상황임.

    부모 컴포넌트가 자식 컴포넌트에게 마이 함수의 매개변수의
    전달하듯이 값을 전달하는 것이 React 에서 가능
    -> props. (properties)

    props 를 이용하면 컴포넌트를 마치 함수를 호출하듯이
    전달하는 값에 따라서 각각 다른 UI를 렌더링하도록
    제어할 수 있다.

    props 는 React 의 핵심 개념 중 하나.
    스프링의 DI 같은 느낌.

    - 매개변수 사용
      - props 는 html 요소나 React 컴포넌트도 전달할 수 있음.
        props 로 전달되는 자식요소는 children 이라는 props 로 전달된다.
      - props 를 이용
        객체의 프로퍼티를 구분해서 사용

      - 객체 구조 분해 할당
        매개변수로 받을 때, 프로퍼티별로
        변수를 초기화해서 사용.

      - 주의점
        전달되는 매개변수 값이 undefine 인 경우에 대해서
        오류가 발생하지 않도록 default 값을 설정해 둠.

### 이벤트 처리
이벤트란? `웹 페이지에서 일어나는 사용자의 행위` <br/>
버튼 클릭, 페이지 스크롤, 새로 고침 등 <br/>

    - 이벤트 핸들링
      이벤트 핸들러 작성해야 함.
      이벤트가 발생하면 특정 코드가 동작이 되도록 함.

    - 이벤트 핸들러 작성 방법
      인라인 : 한 번만 사용 ( button tag 에서 직접 구현 )
      함수 : 재사용 목적 ( button 컴포넌트 내부에 별도의 함수로 구현 )

    - Synthetic Base Event
      모든 웹 브라우저 (크롬, 사파리, 엣지, 파이어폭스, 웨일, 오페라, ...)
      의 이벤트 객체를 하나로 통일 = React (오..)

      브라우저 마다 규격도 다르고 동작 방식도 달라서 생기는 여러가지 문제를
      Cross Browser Issue(브라우저 별 스펙이 달라 발생하는 문제) 라고 부름.
      이 Issue 를 편리하게 해결해 주는 것이 합성 이벤트 (Syntehtic Base Event) 라고 함.

      모든 브라우저에서 사용할 수 있는 통합된 이벤트 규격 객체임.

      개발자 모드 > console > Synthetic Base Event 의 target 속성을 참고

### 컴포넌트와 상태
    상태(State)가 없는 컴포넌트 -> Stateless Component
    
    Stateless Programming
    별도의 State 관리 없이, 함수 logic 및 비동기 처리만으로 상태 관리의 life cycle을 적용하는 프로그래밍

    상태(State) 가 있는 컴포넌트를 작성. -> Stateful Component

    state 는 컴포넌트의 현재 상태를 보관하는 객체.
    state 가 있는 컴포넌트들은 state 의 값에 따라서
    각각 다른 UI 를 화면에 렌더링 하게 됨.

    state 가 변하면, React 가 컴포넌트의 state 의 변화를 감지해서
    자동으로 이 컴포넌트를 다시 렌더링을 해주게 됨.
    => React 에서는 리렌더(Re-Render), 리렌더링(Re-Rendering) 이라고 함.

    Re-Rendering 조건
    1. 컴포넌트 자신이 관리하는 state 값이 변경이 되었을 때
    2. 컴포넌트 자신이 제공받는 props 가 변경이 되었을 때
    3. 부모 컴포넌트가 Re-Rendering 되면,
       자동으로 자식 컴포넌트로 Re-Rendering 됨.

    불필요한 Re-Rendering 은 브라우저 성능에 문제가 됨.
    관련 없는 state 들은 어떻게 관리해야 할지 고민해야 함.

    하나의 컴포넌트에서 다양한 상태 정보를 관리.

## 결론

`Node.js`는 `서버 측에서 자바스크립트를 실행할 수 있는 환경`을 제공하며, `모듈 시스템`을 통해 재사용 가능한 코드를 작성할 수 있게 합니다.<br><br>
`React`는 `컴포넌트 기반의 설계`를 통해 코드의 재사용성을 높이고 유지보수를 용이하게 합니다.

