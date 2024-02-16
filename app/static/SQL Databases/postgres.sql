-- Adminer 4.8.1 PostgreSQL 16.0 (Ubuntu 16.0-1.pgdg22.04+1) dump

DROP TABLE IF EXISTS "banned_products";
DROP SEQUENCE IF EXISTS banned_products_product_id_seq;
CREATE SEQUENCE banned_products_product_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."banned_products" (
    "product_id" integer DEFAULT nextval('banned_products_product_id_seq') NOT NULL,
    "reason" text,
    "created" timestamptz DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "banned_products_pkey" PRIMARY KEY ("product_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "blocked_users";
DROP SEQUENCE IF EXISTS blocked_users_user_id_seq;
CREATE SEQUENCE blocked_users_user_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."blocked_users" (
    "user_id" integer DEFAULT nextval('blocked_users_user_id_seq') NOT NULL,
    "message" text,
    "created" timestamptz DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "blocked_users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "categories";
DROP SEQUENCE IF EXISTS categories_id_seq;
CREATE SEQUENCE categories_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."categories" (
    "id" integer DEFAULT nextval('categories_id_seq') NOT NULL,
    "name" text,
    "slug" text,
    CONSTRAINT "categories_name_key" UNIQUE ("name"),
    CONSTRAINT "categories_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "categories_slug_key" UNIQUE ("slug")
) WITH (oids = false);

INSERT INTO "categories" ("id", "name", "slug") VALUES
(1,	'Electrónicos',	'electronicos'),
(2,	'Ropa',	'ropa'),
(3,	'Libros',	'libros'),
(4,	'Hogar y Jardín',	'hogar-jardin'),
(5,	'Deportes',	'deportes'),
(6,	'Juguetes',	'juguetes'),
(7,	'Automóviles',	'automoviles'),
(8,	'Belleza',	'belleza'),
(9,	'Alimentación',	'alimentacion'),
(10,	'Viajes',	'viajes');

DROP TABLE IF EXISTS "confirmed_orders";
DROP SEQUENCE IF EXISTS confirmed_orders_order_id_seq;
CREATE SEQUENCE confirmed_orders_order_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."confirmed_orders" (
    "order_id" integer DEFAULT nextval('confirmed_orders_order_id_seq') NOT NULL,
    "created" timestamptz DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "confirmed_orders_pkey" PRIMARY KEY ("order_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "orders";
DROP SEQUENCE IF EXISTS orders_id_seq;
CREATE SEQUENCE orders_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orders" (
    "id" integer DEFAULT nextval('orders_id_seq') NOT NULL,
    "product_id" integer NOT NULL,
    "buyer_id" integer NOT NULL,
    "offer" numeric(10,2) NOT NULL,
    "created" timestamptz DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "orders_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "uc_product_buyer" UNIQUE ("product_id", "buyer_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "products";
DROP SEQUENCE IF EXISTS products_id_seq;
CREATE SEQUENCE products_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."products" (
    "id" integer DEFAULT nextval('products_id_seq') NOT NULL,
    "title" text,
    "description" text,
    "photo" text,
    "price" numeric(10,2),
    "category_id" integer,
    "seller_id" integer,
    "created" timestamptz,
    "updated" timestamptz,
    CONSTRAINT "products_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "products" ("id", "title", "description", "photo", "price", "category_id", "seller_id", "created", "updated") VALUES
(1,	'Patata',	'asdasdasd asd sadweafasfasf',	'Never-Gonna-Give-You-Up-Rick-Astley.jpg',	1.00,	1,	1,	NULL,	NULL);

DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "public"."sqlite_sequence" (
    "name" text,
    "seq" integer
) WITH (oids = false);


DROP TABLE IF EXISTS "statuses";
DROP SEQUENCE IF EXISTS statuses_id_seq;
CREATE SEQUENCE statuses_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."statuses" (
    "id" integer DEFAULT nextval('statuses_id_seq') NOT NULL,
    "name" text,
    "slug" text,
    CONSTRAINT "statuses_name_key" UNIQUE ("name"),
    CONSTRAINT "statuses_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "statuses_slug_key" UNIQUE ("slug")
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "name" text,
    "email" text,
    "password" text,
    "created" timestamptz,
    "updated" timestamptz,
    "role" character varying(255),
    "email_token" character(20),
    "verified" character varying(5),
    "token" text,
    "token_expiration" timestamptz,
    CONSTRAINT "users_email_key" UNIQUE ("email"),
    CONSTRAINT "users_name_key" UNIQUE ("name"),
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "users" ("id", "name", "email", "password", "created", "updated", "role", "email_token", "verified", "token", "token_expiration") VALUES
(1,	'User1',	'correo@example.com',	'scrypt:32768:8:1$2eQQJxs7V5km6rnZ$de80c91abf635ca0fcfdd9153c66088b51004338cf8e718903ee1235e9a2ab857610f31c84ad621f6ed7dbd18e87c8334601b0dcd9e4155bff2000396925d50d',	'2024-02-15 18:45:45.957008+00',	'2024-02-15 18:45:45.957008+00',	'admin',	'token123            ',	'true',	'tokenvalor',	'2024-02-16 18:45:45.957008+00');

ALTER TABLE ONLY "public"."banned_products" ADD CONSTRAINT "banned_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."blocked_users" ADD CONSTRAINT "blocked_users_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."confirmed_orders" ADD CONSTRAINT "confirmed_orders_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_buyer_id_fkey" FOREIGN KEY (buyer_id) REFERENCES users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."products" ADD CONSTRAINT "products_category_id_fkey" FOREIGN KEY (category_id) REFERENCES categories(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."products" ADD CONSTRAINT "products_seller_id_fkey" FOREIGN KEY (seller_id) REFERENCES users(id) NOT DEFERRABLE;

-- 2024-02-16 14:33:00.575248+00