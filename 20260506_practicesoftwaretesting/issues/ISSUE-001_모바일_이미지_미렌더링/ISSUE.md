# ISSUE-001: 모바일/태블릿 뷰포트에서 일부 상품 이미지 미렌더링

- **심각도**: P2 Major
- **카테고리**: 반응형 / 콘텐츠
- **발견 일시**: 2026-05-06
- **URL**: https://practicesoftwaretesting.com/
- **재현 조건**: 뷰포트 375×812 (모바일), 768×1024 (태블릿)

## 현상
hammer01~04.avif 이미지(Claw Hammer with Shock Reduction Grip, Hammer, Claw Hammer, Thor Hammer)가
모바일·태블릿 뷰포트에서 빈 흰색 박스로 표시됨.
JavaScript `naturalWidth` 검사에서는 `broken: false`로 반환되나 화면에 렌더링되지 않음.

## 예상 동작
모든 뷰포트에서 상품 이미지가 정상 렌더링되어야 함.

## 재현 방법
1. 브라우저 뷰포트를 375px 또는 768px로 설정
2. https://practicesoftwaretesting.com/ 접속
3. 스크롤 하여 hammer 계열 상품 확인 → 이미지 영역이 빈 흰색으로 표시됨

## 데스크톱(1280px)에서는 정상
1280px 뷰포트에서는 동일 이미지가 모두 정상 렌더링됨.
뷰포트 크기에 따른 lazy loading 또는 AVIF 디코딩 타이밍 이슈로 추정.

## 스크린샷
![screenshot](./screenshot.png)

## 비고
- 영향 상품: Claw Hammer with Shock Reduction Grip, Hammer, Claw Hammer, Thor Hammer (4개)
- 정상 상품: Combination Pliers, Pliers, Bolt Cutters, Long Nose Pliers, Slip Joint Pliers (5개)
- AVIF 포맷의 모바일 렌더링 최적화 검토 필요
