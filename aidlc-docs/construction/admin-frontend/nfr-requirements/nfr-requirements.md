# Admin Frontend - NFR Requirements

## Tech Stack (Same as Customer Frontend)

- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State**: Composition API
- **Routing**: Vue Router 4
- **HTTP**: Axios
- **WebSocket**: Native WebSocket API

## Key NFR Requirements

### Performance
- Page Load: < 3초
- Bundle Size: < 600KB (gzipped)

### Security
- JWT 토큰 (SessionStorage)
- Authorization header
- Token expiration: 8시간

### Usability
- Desktop-first design (1024px+)
- Responsive down to 768px
- Keyboard shortcuts for common actions

### Reliability
- WebSocket reconnection on disconnect
- Auto-refresh on network recovery
- Optimistic UI updates

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-09  
**Status**: Draft
