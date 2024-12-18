--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: storeapp_order; Type: TABLE; Schema: django; Owner: alex6damian
--

CREATE TABLE django.storeapp_order (
    order_id integer NOT NULL,
    quantity integer NOT NULL,
    order_date date NOT NULL
);


ALTER TABLE django.storeapp_order OWNER TO alex6damian;

--
-- Name: storeapp_order_order_id_seq; Type: SEQUENCE; Schema: django; Owner: alex6damian
--

ALTER TABLE django.storeapp_order ALTER COLUMN order_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME django.storeapp_order_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: storeapp_order; Type: TABLE DATA; Schema: django; Owner: alex6damian
--

COPY django.storeapp_order (order_id, quantity, order_date) FROM stdin;
1	1	2024-11-07
\.


--
-- Name: storeapp_order_order_id_seq; Type: SEQUENCE SET; Schema: django; Owner: alex6damian
--

SELECT pg_catalog.setval('django.storeapp_order_order_id_seq', 1, true);


--
-- Name: storeapp_order storeapp_order_pkey; Type: CONSTRAINT; Schema: django; Owner: alex6damian
--

ALTER TABLE ONLY django.storeapp_order
    ADD CONSTRAINT storeapp_order_pkey PRIMARY KEY (order_id);


--
-- PostgreSQL database dump complete
--

