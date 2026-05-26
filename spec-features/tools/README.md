# AI Skills đọc LME Spec

Thư mục này chứa 6 AI skills giúp đọc spec LME hiệu quả theo vai trò. Mỗi skill là file `.md` dùng làm prompt cho Claude Code (hoặc AI agent tương tự).

---

## Skills có sẵn

| Skill | File | Dành cho | Mô tả |
|-------|------|----------|-------|
| `/read-spec` | [read-spec.md](read-spec.md) | Tất cả | Tổng quan tính năng, trạng thái, gợi ý skill tiếp theo |
| `/read-spec-ui` | [read-spec-ui.md](read-spec-ui.md) | Frontend dev | Màn hình, form fields, user flows, shared components |
| `/read-spec-api` | [read-spec-api.md](read-spec-api.md) | Backend dev | Endpoints, params, responses, validation, errors |
| `/read-spec-logic` | [read-spec-logic.md](read-spec-logic.md) | Backend dev | Business rules, controllers, models, services, jobs |
| `/read-spec-db` | [read-spec-db.md](read-spec-db.md) | Backend / DBA | Tables, relationships, enums, field traceability |
| `/read-spec-test` | [read-spec-test.md](read-spec-test.md) | QA / Tester | Test scenarios, error cases, edge cases, assertions |

---

## Cách sử dụng trong project khác

### Bước 1: Clone / mount spec repo

Clone hoặc thêm submodule repo spec vào project của bạn:

```bash
# Ví dụ: clone vào docs/lme-spec/
git clone <spec-repo-url> docs/lme-spec

# Hoặc dùng git submodule
git submodule add <spec-repo-url> docs/lme-spec
```

### Bước 2: Cấu hình trong CLAUDE.md

Trong file `CLAUDE.md` của project, thêm hướng dẫn cho AI agent:

```markdown
## LME Spec Reference

Spec hệ thống LME nằm tại `docs/lme-spec/`.
- Hướng dẫn đọc: `docs/lme-spec/GUIDE.md`
- Skills đọc spec: `docs/lme-spec/tools/`

Khi cần đọc spec tính năng LME, sử dụng skills trong `docs/lme-spec/tools/`:
- Đọc file skill tương ứng để biết cách thực hiện
- SPEC_BASE_PATH = docs/lme-spec
```

### Bước 3: Tham chiếu skills

Có 2 cách tham chiếu:

**Cách 1 — Symlink** (khuyến nghị): Tạo symlink từ `.claude/skills/` đến tools/:
```bash
# Từ root project
ln -s ../../docs/lme-spec/tools/read-spec.md .claude/skills/read-spec.md
ln -s ../../docs/lme-spec/tools/read-spec-ui.md .claude/skills/read-spec-ui.md
# ... tương tự cho các skill khác
```

**Cách 2 — Hướng dẫn trong CLAUDE.md**: Chỉ cần ghi rõ path trong CLAUDE.md, AI agent sẽ đọc file skill trực tiếp khi được yêu cầu.

---

## Cách sử dụng

```
/read-spec tag-management       # Tìm theo tên folder (kebab-case)
/read-spec FA-012                # Tìm theo mã tính năng
/read-spec-ui chat-1on1          # Đọc UI spec cho frontend
/read-spec-api auto-reply        # Đọc API spec cho backend
/read-spec-logic notify-setting  # Đọc logic + jobs cho backend
/read-spec-db tag-management     # Đọc DB mapping
/read-spec-test auto-reply       # Đọc spec để viết test cases
```

### Workflow đề xuất theo vai trò

**Frontend Developer**:
1. `/read-spec {feature}` — hiểu tổng quan
2. `/read-spec-ui {feature}` — chi tiết màn hình, forms, flows
3. Kiểm tra shared components nếu spec có tham chiếu SC-XXX

**Backend Developer**:
1. `/read-spec {feature}` — hiểu tổng quan
2. `/read-spec-api {feature}` — endpoints cần implement
3. `/read-spec-logic {feature}` — business logic + jobs
4. `/read-spec-db {feature}` — database schema

**QA / Tester**:
1. `/read-spec {feature}` — hiểu tổng quan + scope
2. `/read-spec-test {feature}` — test scenarios, edge cases, error cases

**Tech Lead / PM**:
1. `/read-spec {feature}` — overview, scope, cross-references, gaps

---

## Cấu hình SPEC_BASE_PATH

Mỗi skill cần biết đường dẫn đến thư mục chứa specs. Cơ chế tìm:

1. **Tự động**: Skill tìm file `admin/index.md` hoặc `system-admin/index.md` trong thư mục cha gần nhất
2. **Cấu hình**: Đặt `SPEC_BASE_PATH` trong CLAUDE.md của project — VD: `SPEC_BASE_PATH=docs/lme-spec`
3. **Mặc định**: Nếu skill nằm trong `features/tools/`, path mặc định là `features/` (thư mục cha)
