insert into "user" (user_name, user_email, user_password)
values (
        "Test User",
        "test@example.com",
        -- Test_Password_42
        "scrypt:32768:8:1$kll4pHFhNW2SjcAy$7a450ef6042d8df11222c72ac9afd85d8469e9890f992a9d6056582a68ad93ece4bcd029e0c7a2d591ee0d957488c15161a5f8e619cfbfdd57a76aa56fb7171b"
    ),
    (
        "Alice Wang",
        "alice@alicesmith.net",
        -- password123
        "scrypt:32768:8:1$ycgvLQY5rRAyl7ya$129a11a08d493f2d0db32d8bc09cff5412ea4bbb2b4a1e9a4769e90e7a95efe7f45d89f7830fd8e2dc21c16972444b01ec35337dc3c9909487665e0ec524e4a9"
    ),
    (
        "Bob Smith",
        "bobsmith57@gmail.com",
        -- qwerty
        "scrypt:32768:8:1$8Wm3hUKi2xxQxqso$945d4781fd32fdb9c32de4a2295939af600e6c6f3fc0f3cfeb9fe0e718a8eacc7a763cab566c4ec871db2fd510e4fed7f71a57a7aaab5e387ec9d650801c0936"
    );
