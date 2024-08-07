---
title: 자주 쓰는/쓰일 Git 명령어 모음
description: git bash 잘 쓰고 싶어요
date: 2024-08-07 00:11:50 +09:00
categories: [git, command]
pin : true
tags:
  [
    Git,
    Git Bash,
    Tip
  ]
---

### 글 작성 이유
써야할 일이 종종 생기는데, 매번 외워지지는 않고.. 찾기는 귀찮고.. 해서 <br>
자주 쓰이는 것들은 모아두고 보자 마인드로 쓰게 되었습니다. <br>
git bash 잘 쓰면 좋잖아요 ^^ 외워봅시다.

# 자주 쓰는 commands


## 커밋 관련

모든 파일 git stage 추가 <br>
`$ git add .`<br>

stage 추가 된 파일 commit<br>
`$ git commit -m "커밋내용"`<br>

origin에 존재하는 branch로 push 보통 초기에는 master branch를 사용한다.<br>
`$ git push origin {branch명}`<br>

## 조회 관련<br>
stage 추가 된 파일 목록 조회<br>
`$ git status`<br>

ssss<br>
`$ git log`<br>

삭제된 커밋을 포함한 모든 히스토리 조회<br>
`$ git reflog`<br>

## 브랜치 관련

새로운 브랜치 생성<br>
`$ git branch {브랜치명}`<br>


다른 브랜치로 전환<br>
`$ git checkout {브랜치명}`<br>


브랜치 생성 및 전환<br>
`$ git checkout -b {브랜치명}`<br>


로컬 브랜치 삭제<br>
`$ git branch -d {브랜치명}`<br>

원격 브랜치 삭제<br>
`$ git push origin --delete {브랜치명}`<br>

## 병합 관련

다른 브랜치를 현재 브랜치로 병합<br>
`$ git merge {브랜치명}`<br>


병합 충돌 해결 후 병합 마무리<br>
`$ git add {충돌 파일}`<br>
`$ git commit`<br>


## 원격 저장소 관련

원격 저장소 추가<br>
`$ git remote add origin {원격 저장소 URL}`<br>


원격 저장소 목록 조회<br>
`$ git remote -v`<br>


원격 저장소 URL 변경<br>
`$ git remote set-url origin {새 원격 저장소 URL}`<br>


## 기타 유용한 명령어

변경 사항 취소 (stage에 추가하지 않은 파일들)<br>
`$ git checkout -- {파일명}`<br>


가장 최근 커밋 수정 (커밋 메시지 포함)<br>
`$ git commit --amend`<br>


특정 커밋으로 되돌리기<br>
`$ git reset --hard {커밋 해시}`<br>


변경 사항 stash (임시로 저장)<br>
`$ git stash`<br>


stash된 변경 사항 적용<br>
`$ git stash pop`<br>

### 추가적인 좋은 기능이 있다면 댓글 남겨주시면 감사하겠습니다 😀


