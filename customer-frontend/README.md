# Table Order - Customer Frontend

고객용 테이블 오더 프론트엔드 애플리케이션

## Tech Stack

- Vue 3 (Composition API)
- Vite
- Vue Router 4
- Tailwind CSS
- Axios
- html5-qrcode

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

### 3. Run Development Server

```bash
npm run dev
```

서버가 http://localhost:5173 에서 실행됩니다.

## Build

```bash
npm run build
```

빌드된 파일은 `dist/` 폴더에 생성됩니다.

## Project Structure

```
src/
├── components/
│   ├── atoms/          # 기본 UI 컴포넌트
│   ├── molecules/      # 조합 컴포넌트
│   └── organisms/      # 복잡한 컴포넌트
├── pages/              # 페이지 컴포넌트
├── composables/        # Composition API 로직
├── api/                # API 클라이언트
├── router/             # Vue Router 설정
├── assets/             # 정적 파일
└── main.js             # 앱 진입점
```

## Features

- 📱 QR 코드 테이블 로그인
- 🍔 카테고리별 메뉴 탐색
- 🛒 장바구니 관리
- 💰 팁 선택 (0%, 5%, 10%, 15%, 20%)
- 📊 실시간 주문 상태 확인
- 🔔 알러지 정보 표시

## License

MIT
