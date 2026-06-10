# Guided Postman Lab — WebServiceFastAPIExample

**Duration:** ~75 minutes  
**Goal:** Test the full system end-to-end using Postman and understand how auth, DB, cache, and external APIs work together.

---

## Before you start

### 1. Start services

```powershell
cd WebServiceFastAPIExample
docker compose up -d
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### 2. Import Postman collection

1. Open Postman  
2. **Import** → `resources/postman/WebServiceFastAPIExample.postman_collection.json`  
3. Confirm collection variable `baseUrl` = `http://localhost:8000`

### 3. Open Swagger (optional reference)

http://localhost:8000/docs

---

## Part A — Authentication (20 min)

### Exercise A1 — Register a new user

| Field | Value |
|-------|-------|
| **Request** | `POST {{baseUrl}}/user/` |
| **Body type** | `raw` → **JSON** |

```json
{
  "username": "YOUR_NAME",
  "first_name": "Your",
  "last_name": "Name",
  "password": "12qwaszx"
}
```

> Replace `YOUR_NAME` with something unique (e.g. `student_alon`).

**Checkpoint A1**

- [ ] Status code is **201 Created**
- [ ] Response body is empty (no error)

**Question:** Why is this endpoint **not** protected by a token?

---

### Exercise A2 — Login and receive a JWT

| Field | Value |
|-------|-------|
| **Request** | `POST {{baseUrl}}/auth/token` |
| **Body type** | **x-www-form-urlencoded** (NOT JSON) |

| Key | Value |
|-----|-------|
| username | (same as A1) |
| password | `12qwaszx` |

**Checkpoint A2**

- [ ] Status code is **200 OK**
- [ ] Response contains `"jwt_token": "eyJ..."`
- [ ] Collection variable `token` was saved (check collection Variables tab)

**Question:** Why must login use **form data** instead of JSON? (Hint: `OAuth2PasswordRequestForm`)

---

### Exercise A3 — Call a protected endpoint

| Field | Value |
|-------|-------|
| **Request** | `GET {{baseUrl}}/user/1` |
| **Authorization** | Bearer Token → `{{token}}` |

**Checkpoint A3**

| Test | Expected status |
|------|-----------------|
| With valid token | **200** |
| Without Authorization header | **401** |
| With fake token `Bearer abc123` | **401** |

**Question:** What does `Depends(auth_service.validate_user)` do before your handler runs?

---

### Exercise A4 — Negative test: duplicate username

Repeat **A1** with the **same username**.

**Checkpoint A4**

- [ ] Status code is **400**
- [ ] Detail message mentions username already taken

---

## Part B — Customer + Redis cache (15 min)

### Exercise B1 — Create a customer

| Field | Value |
|-------|-------|
| **Request** | `POST {{baseUrl}}/customer/` |
| **Body** | JSON |

```json
{
  "first_name": "Alon",
  "last_name": "Shaked",
  "email": "alon@gmail.com",
  "status": "REGULAR"
}
```

**Checkpoint B1**

- [ ] Status **200**
- [ ] Response text: `customer creation is complete`

---

### Exercise B2 — List all customers

| Field | Value |
|-------|-------|
| **Request** | `GET {{baseUrl}}/customer/` |

**Checkpoint B2**

- [ ] Response is a JSON **array**
- [ ] Your new customer appears with an `id`
- [ ] Write down the `id`: __________ (use it as `customerId` in later steps)

---

### Exercise B3 — Cache behavior

| Field | Value |
|-------|-------|
| **Request** | `GET {{baseUrl}}/customer/{id}` |

Run the **same request twice**.

**Checkpoint B3**

- [ ] Both calls return **200** with the same customer data
- [ ] In the server terminal, the **second** call should be faster (data comes from Redis)

**Question:** Which repository method reads from cache first? Which method writes to cache after a DB read?

---

### Exercise B4 — VIP limit (optional challenge)

Try creating **11 customers** with `"status": "VIP"`.

**Checkpoint B4**

- [ ] The 11th VIP customer returns **403**

---

## Part C — Customer orders (15 min)

### Exercise C1 — Create order for a new customer

| Field | Value |
|-------|-------|
| **Request** | `POST {{baseUrl}}/customer_order/` |
| **Body** | JSON |

```json
{
  "customer": {
    "first_name": "Dana",
    "last_name": "Cohen",
    "email": "dana@gmail.com",
    "status": "REGULAR"
  },
  "customer_order": {
    "item_name": "Laptop",
    "price": 1699.99
  }
}
```

**Checkpoint C1**

- [ ] Status **200**
- [ ] Response has `customer` and `customer_orders` (array)
- [ ] `customer_orders` contains the Laptop item

**Question:** Why does the request send `item_name` but the DB stores `customer_id` + `item_id` for favorites? (Different feature — think about customer_order vs favorite.)

---

### Exercise C2 — Get order by id

| Field | Value |
|-------|-------|
| **Request** | `GET {{baseUrl}}/customer_order/1` |

**Checkpoint C2**

- [ ] Returns a single order object with `id`, `customer_id`, `item_name`, `price`

---

### Exercise C3 — Update order (404 test)

| Field | Value |
|-------|-------|
| **Request** | `PUT {{baseUrl}}/customer_order/999` |
| **Body** | Same JSON as C1 |

**Checkpoint C3**

- [ ] Status **404** (order does not exist)

---

### Exercise C4 — Delete customer with orders

Try `DELETE {{baseUrl}}/customer/1` if that customer has orders.

**Checkpoint C4**

- [ ] What happens? ___________________________
- [ ] Why? (Hint: foreign key in `init.sql`)

---

## Part D — Student API (10 min)

### Exercise D1 — Full CRUD cycle

Complete this table:

| Step | Method | URL | Status expected |
|------|--------|-----|-----------------|
| Create | POST | `/student/` | 200 |
| List all | GET | `/student/` | 200 |
| Get one | GET | `/student/1` | 200 |
| Update | PUT | `/student/1` | 200 |
| Delete | GET | `/student/1` | **404** |

**Create body:**

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com"
}
```

**Checkpoint D1**

- [ ] All steps completed in order
- [ ] After delete, GET returns 404

---

## Part E — External API (5 min)

### Exercise E1 — TV Maze

| Field | Value |
|-------|-------|
| **Request** | `GET {{baseUrl}}/tv_maze/show/1` |

**Checkpoint E1**

- [ ] Status **200** (or `null` body if show not found — check your implementation)
- [ ] Response includes `tv_show_name`

**Question:** Does this call hit **your database** or an **external API**?

---

## Part F — Redis direct test (5 min)

### Exercise F1

| Field | Value |
|-------|-------|
| **Request** | `POST {{baseUrl}}/redis/test?redis_key=lab_key&redis_value=hello` |

**Checkpoint F1**

- [ ] Response: `{"message": "Redis test is complete"}`

---

## Part G — Customer favorites (bonus, 10 min)

> Requires seller service running at `http://localhost:8081`

### Exercise G1 — Add favorite

| Field | Value |
|-------|-------|
| **Request** | `POST {{baseUrl}}/customer_favorite/` |

```json
{
  "customer_id": 1,
  "item_name": "Laptop"
}
```

**Checkpoint G1**

- [ ] Returns a numeric id, or `null` if seller service is down / item not found

**Question:** Why does the service call `seller_service_api` before saving to the DB?

---

## Final submission checklist

Hand in a screenshot or exported Postman results showing:

1. ✅ Login response with `jwt_token`
2. ✅ Protected `GET /user/1` with Bearer token (200)
3. ✅ `GET /user/1` without token (401)
4. ✅ Created customer in `GET /customer/`
5. ✅ Created customer order response
6. ✅ Student delete → subsequent GET returns 404

---

## Reflection questions (write 1–2 sentences each)

1. What is the difference between **401** and **404** in this project? Give one example of each.
2. Why do we use a **service layer** between controller and repository?
3. What are two things that are stored in the JWT payload in this project?
4. When would you use **form data** vs **JSON** in Postman for this API?

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Connection refused | API not running | Start `uvicorn main:app --reload` |
| 500 on DB calls | MySQL not up | `docker compose up -d` |
| Form error on `/auth/token` | Body set to JSON | Switch to x-www-form-urlencoded |
| bcrypt / password error | Wrong bcrypt version | `pip install bcrypt==4.0.1` |
| Customer favorite returns null | Seller service down | Start seller service on port 8081 |
