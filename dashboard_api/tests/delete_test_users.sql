SET SQL_SAFE_UPDATES = 0;

-- Delete related Customer profiles for users except id=1
DELETE FROM core_customer WHERE user_id IN (SELECT id FROM auth_user WHERE id <> 1);

-- Delete users except id=1
DELETE FROM auth_user WHERE id <> 1; 